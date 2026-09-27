"""OpenAI judging, shared by the HN crawler and the CMS research page.

The crawler judges a story title in one blocking call. Research runs the same bar with web
search on, as a background response: `start()` returns at once, and `refresh()` collects the
verdict whenever the research page is next loaded.
"""

import json
from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import transaction
from django.utils.text import slugify

from syllabus.editorial import RESEARCH_RUBRIC
from syllabus.models import Category, ResearchStatus, Status, Subject, TopicResearch, Verdict

SUBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "is_new_subject": {
            "type": "boolean",
            "description": "True only if this unlocks something that was impossible or "
            "wildly impractical before, and is not already covered by an existing subject.",
        },
        "duplicate_of_slug": {
            "type": ["string", "null"],
            "description": "Slug of the existing subject this duplicates, or null.",
        },
        "reason": {
            "type": "string",
            "description": "One or two sentences justifying the verdict.",
        },
        "title": {"type": "string"},
        "slug": {"type": "string", "description": "lowercase-hyphenated, max 60 chars"},
        "one_liner": {"type": "string", "description": "What it is, one plain sentence."},
        "what_you_can_build": {
            "type": "string",
            "description": "3-4 concrete things, one per line, no bullet characters.",
        },
        "before_this": {"type": "string", "description": "How people did this before."},
        "why_new": {
            "type": "string",
            "description": "What specifically was impossible or impractical before.",
        },
        "category": {"type": "string", "enum": [c.value for c in Category]},
    },
    "required": [
        "is_new_subject",
        "duplicate_of_slug",
        "reason",
        "title",
        "slug",
        "one_liner",
        "what_you_can_build",
        "before_this",
        "why_new",
        "category",
    ],
    "additionalProperties": False,
}

RESEARCH_FIELDS = {
    "became_usable_on": {
        "type": ["string", "null"],
        "description": "YYYY-MM-DD when ordinary people could first use it, or null.",
    },
    "date_note": {"type": "string", "description": "Only when the date is a judgement call."},
    "source_url": {"type": "string", "description": "The announcement that dates it."},
    "resource_url": {"type": "string", "description": "Where a newcomer should start."},
    "sources": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Every URL the verdict relies on.",
    },
}

# Strict mode wants every property listed as required, so the extras are appended, not optional.
RESEARCH_SCHEMA = {
    **SUBJECT_SCHEMA,
    "properties": {**SUBJECT_SCHEMA["properties"], **RESEARCH_FIELDS},
    "required": SUBJECT_SCHEMA["required"] + list(RESEARCH_FIELDS),
}

URL_MAX = 200  # Django's URLField default; a longer URL would fail the insert on Postgres.
_is_url = URLValidator(schemes=["http", "https"])


def get_client():
    if not settings.OPENAI_API_KEY:
        return None
    import openai

    return openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def subject_index():
    rows = Subject.objects.values_list("slug", "title", "one_liner")
    return "\n".join(f"- {slug}: {title} — {one_liner}" for slug, title, one_liner in rows)


def json_format(name, schema):
    return {"format": {"type": "json_schema", "name": name, "strict": True, "schema": schema}}


def parse(response):
    """The model's JSON verdict, or None if it refused."""
    # Reasoning tokens count against max_output_tokens, so a truncated run is possible.
    if response.status == "incomplete":
        raise RuntimeError(f"incomplete response: {response.incomplete_details.reason}")

    # output[] holds reasoning and web_search_call items too; only the message carries the JSON.
    message = next((item for item in response.output if item.type == "message"), None)
    part = message.content[0] if message and message.content else None
    if part is None or part.type == "refusal":
        return None
    return json.loads(part.text)


def safe_url(url):
    """Model output is shaped by whatever pages it read, so its URLs are untrusted.

    Anything that is not a plain http(s) link is dropped: a `javascript:` URL would otherwise
    end up as a clickable link on the public site.
    """
    url = (url or "").strip()
    if len(url) > URL_MAX:
        return ""
    try:
        _is_url(url)
    except ValidationError:
        return ""
    return url


def create_draft(data, source_url):
    base = slugify(data.get("slug") or data["title"])[:60] or "untitled"
    slug, n = base, 2
    while Subject.objects.filter(slug=slug).exists():
        slug = f"{base[:57]}-{n}"
        n += 1
    category = data.get("category")
    if category not in Category.values:
        category = Category.BUILD
    try:
        became_usable_on = date.fromisoformat(data.get("became_usable_on") or "")
    except ValueError:
        became_usable_on = None
    return Subject.objects.create(
        slug=slug,
        title=data["title"][:160],
        one_liner=data["one_liner"][:300],
        what_you_can_build=data["what_you_can_build"],
        before_this=data["before_this"],
        why_new=data["why_new"],
        category=category,
        status=Status.DRAFT,
        source_url=source_url,
        resource_url=safe_url(data.get("resource_url")),
        became_usable_on=became_usable_on,
        date_note=(data.get("date_note") or "")[:300],
    )


# --- research --------------------------------------------------------------


def start(client, topic, url):
    link = f"\nLink: {url}" if url else ""
    return client.responses.create(
        model=settings.SYLLABUS_CRAWLER_MODEL,
        background=True,
        tools=[{"type": "web_search"}],
        reasoning={"effort": "medium"},
        # Web search results and reasoning both eat into this, so it is far above the crawler's.
        max_output_tokens=16000,
        instructions=f"{RESEARCH_RUBRIC}\n\nSubjects already in the syllabus:\n{subject_index()}",
        input=[
            {
                "role": "user",
                "content": f"Topic: {topic}{link}\n\nResearch it. Does it belong in the syllabus?",
            }
        ],
        text=json_format("syllabus_research", RESEARCH_SCHEMA),
    )


def refresh(research, client):
    """Collect a finished background response. A no-op while OpenAI is still working."""
    response = client.responses.retrieve(research.response_id)
    if response.status in ("queued", "in_progress"):
        return

    # The network call stays outside the lock. Two tabs polling at once both get here; only
    # the first to take the row lock still sees RUNNING, so only one draft is filed.
    with transaction.atomic():
        row = TopicResearch.objects.select_for_update().get(pk=research.pk)
        if row.status != ResearchStatus.RUNNING:
            return
        try:
            # A savepoint: if create_draft hits a DB error, the outer transaction can still
            # record the failure instead of being poisoned by it.
            with transaction.atomic():
                finish(row, response)
        except Exception as exc:
            row.status, row.verdict, row.error = ResearchStatus.FAILED, "", str(exc)
        row.save()


def finish(row, response):
    if response.status != "completed":
        error = getattr(response, "error", None)
        raise RuntimeError(getattr(error, "message", None) or f"response {response.status}")

    data = parse(response)
    row.status = ResearchStatus.DONE
    if data is None:
        row.verdict, row.reason = Verdict.REJECTED_LLM, "Model declined to judge this topic."
        return

    data["sources"] = [url for url in map(safe_url, data.get("sources") or []) if url]
    row.result, row.reason = data, data.get("reason", "")
    if data.get("duplicate_of_slug"):
        row.verdict = Verdict.DUPLICATE
    elif not data.get("is_new_subject"):
        row.verdict = Verdict.REJECTED_LLM
    else:
        row.verdict = Verdict.ACCEPTED
        row.subject = create_draft(data, draft_source(row))


def draft_source(row):
    return safe_url(row.result.get("source_url")) or row.url
