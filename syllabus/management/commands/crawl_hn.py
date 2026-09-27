"""Daily Hacker News crawl: propose new syllabus subjects, as drafts.

Pipeline: fetch -> free keyword prefilter -> one OpenAI call per survivor -> draft Subject.
Every story we look at is recorded in CrawlCandidate keyed by its HN id, so a story is
never fetched, judged, or paid for twice.
"""

import logging
import re
import time

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand

from syllabus import judge
from syllabus.editorial import RUBRIC
from syllabus.models import CrawlCandidate, Verdict

logger = logging.getLogger(__name__)

ALGOLIA = "https://hn.algolia.com/api/v1"
HN_ITEM_URL = "https://news.ycombinator.com/item?id={}"

# A title has to touch at least one of these to be worth a paid judgement call.
KEYWORDS = {
    "ai",
    "llm",
    "llms",
    "gpt",
    "claude",
    "gemini",
    "llama",
    "mistral",
    "deepseek",
    "qwen",
    "model",
    "models",
    "agent",
    "agents",
    "agentic",
    "rag",
    "mcp",
    "embedding",
    "embeddings",
    "prompt",
    "prompting",
    "inference",
    "transformer",
    "diffusion",
    "generative",
    "genai",
    "multimodal",
    "fine-tune",
    "finetune",
    "fine-tuning",
    "lora",
    "quantization",
    "quantized",
    "vector",
    "openai",
    "anthropic",
    "huggingface",
    "ollama",
    "vllm",
    "whisper",
    "tts",
    "speech",
    "voice",
    "vision",
    "ocr",
    "copilot",
    "cursor",
    "codegen",
    "neural",
    "ml",
    "machine-learning",
    "chatbot",
    "assistant",
    "reasoning",
    "context",
    "tokens",
    "gpu",
}


class Command(BaseCommand):
    help = "Crawl Hacker News for genuinely new AI subjects and file them as drafts."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=12, help="Max stories to judge.")
        parser.add_argument("--min-points", type=int, default=40, help="HN score floor.")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Prefilter only: print what would be judged, make no API calls, write nothing.",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        min_points = options["min_points"]
        dry_run = options["dry_run"]

        stories = self.fetch_stories(min_points)
        self.stdout.write(f"Fetched {len(stories)} story/stories from Hacker News.")

        seen = set(CrawlCandidate.objects.values_list("hn_id", flat=True))
        survivors, skipped = self.prefilter(stories, seen, min_points)

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run — nothing written, no API calls."))
            for story in survivors[:limit]:
                self.stdout.write(f"  would judge: [{story['points']:>4}] {story['title']}")
            already_seen = len(stories) - len(survivors) - len(skipped)
            self.stdout.write(
                f"fetched {len(stories)}, already seen {already_seen}, "
                f"filtered out {len(skipped)}, would judge {min(len(survivors), limit)}"
            )
            return

        for story in skipped:
            self.record(story, Verdict.SKIPPED_HEURISTIC, "Off-topic or below the points floor.")

        batch = survivors[:limit]
        if not batch:
            self.stdout.write(self.style.SUCCESS("Nothing new worth judging today."))
            return

        client = judge.get_client()
        if client is None:
            self.stdout.write(
                self.style.WARNING(
                    f"OPENAI_API_KEY is not set — {len(batch)} candidate(s) left unjudged. "
                    "They will be picked up on the next run once the key is configured."
                )
            )
            return

        index = judge.subject_index()
        accepted = 0
        for story in batch:
            try:
                accepted += int(bool(self.judge(client, story, index)))
            except Exception as exc:  # one bad story must not kill the run
                logger.exception("Failed to judge HN story %s", story["hn_id"])
                self.stdout.write(self.style.ERROR(f"  ! {story['title']}: {exc}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"fetched {len(stories)}, filtered out {len(skipped)}, judged {len(batch)}, "
                f"accepted {accepted} (drafts — review at /dashboard/subjects/?status=draft)"
            )
        )

    # --- fetch -------------------------------------------------------------

    def fetch_stories(self, min_points):
        day_ago = int(time.time()) - 24 * 60 * 60
        queries = [
            {"tags": "front_page"},
            {
                "tags": "story",
                "numericFilters": f"points>{min_points},created_at_i>{day_ago}",
                "hitsPerPage": 100,
            },
        ]
        stories, seen_ids = [], set()
        with httpx.Client(timeout=20.0) as http:
            for params in queries:
                path = "search" if params.get("tags") == "front_page" else "search_by_date"
                try:
                    response = http.get(f"{ALGOLIA}/{path}", params=params)
                    response.raise_for_status()
                except httpx.HTTPError as exc:
                    self.stdout.write(self.style.ERROR(f"HN fetch failed ({path}): {exc}"))
                    continue
                for hit in response.json().get("hits", []):
                    hn_id = str(hit.get("objectID", ""))
                    if not hn_id or hn_id in seen_ids or not hit.get("title"):
                        continue
                    seen_ids.add(hn_id)
                    stories.append(
                        {
                            "hn_id": hn_id,
                            "title": hit["title"],
                            "url": hit.get("url") or HN_ITEM_URL.format(hn_id),
                            "points": hit.get("points") or 0,
                        }
                    )
        return stories

    # --- prefilter (free) --------------------------------------------------

    def prefilter(self, stories, seen, min_points):
        survivors, skipped = [], []
        for story in stories:
            if story["hn_id"] in seen:
                continue
            words = set(re.findall(r"[a-z0-9\-]+", story["title"].lower()))
            if story["points"] < min_points or not (words & KEYWORDS):
                skipped.append(story)
            else:
                survivors.append(story)
        survivors.sort(key=lambda s: s["points"], reverse=True)
        return survivors, skipped

    # --- judge -------------------------------------------------------------

    def judge(self, client, story, index):
        # RUBRIC + index lead the instructions so OpenAI's automatic prefix caching can hit;
        # there is no explicit cache marker to set.
        response = client.responses.create(
            model=settings.SYLLABUS_CRAWLER_MODEL,
            max_output_tokens=4000,
            reasoning={"effort": "low"},
            instructions=f"{RUBRIC}\n\nSubjects already in the syllabus:\n{index}",
            input=[
                {
                    "role": "user",
                    "content": (
                        f"Hacker News story ({story['points']} points)\n"
                        f"Title: {story['title']}\n"
                        f"URL: {story['url']}\n\n"
                        "Does this belong in the syllabus?"
                    ),
                }
            ],
            text=judge.json_format("syllabus_subject", judge.SUBJECT_SCHEMA),
        )

        data = judge.parse(response)
        if data is None:
            self.record(story, Verdict.REJECTED_LLM, "Model declined to judge this story.")
            self.stdout.write(f"  - {story['title']} (declined)")
            return None

        if data.get("duplicate_of_slug"):
            self.record(story, Verdict.DUPLICATE, data.get("reason", ""))
            self.stdout.write(f"  = {story['title']} -> {data['duplicate_of_slug']}")
            return None

        if not data.get("is_new_subject"):
            self.record(story, Verdict.REJECTED_LLM, data.get("reason", ""))
            self.stdout.write(f"  - {story['title']}")
            return None

        subject = judge.create_draft(data, story["url"])
        self.record(story, Verdict.ACCEPTED, data.get("reason", ""), subject=subject)
        self.stdout.write(self.style.SUCCESS(f"  + draft: {subject.slug} — {subject.title}"))
        return subject

    # --- persistence -------------------------------------------------------

    def record(self, story, verdict, reason, subject=None):
        CrawlCandidate.objects.update_or_create(
            hn_id=story["hn_id"],
            defaults={
                "hn_title": story["title"][:500],
                "hn_url": story["url"],
                "points": story["points"],
                "verdict": verdict,
                "reason": reason or "",
                "subject": subject,
            },
        )
