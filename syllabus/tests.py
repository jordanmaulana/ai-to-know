import json
from datetime import date
from io import StringIO
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from syllabus.forms import SubjectForm
from syllabus.management.commands.crawl_hn import Command as CrawlCommand
from syllabus.models import (
    Category,
    CrawlCandidate,
    ResearchStatus,
    Status,
    Subject,
    TopicResearch,
    Verdict,
)
from syllabus.seed_data import SUBJECTS

VALID = {
    "title": "Retrieval augmented generation",
    "slug": "",
    "category": Category.BUILD,
    "became_usable_on": "2023-01-15",
    "one_liner": "Answer questions from your own documents.",
    "what_you_can_build": "A search box over your handbook\nA support bot that cites sources",
    "before_this": "You read the documents yourself.",
    "why_new": "No search index could answer in prose before.",
    "resource_url": "",
    "source_url": "",
}


def make_subject(**overrides):
    fields = {
        "slug": "example",
        "title": "Example",
        "one_liner": "An example.",
        "what_you_can_build": "One thing\nAnother thing",
        "before_this": "Nothing.",
        "why_new": "Everything.",
        "category": Category.BUILD,
        "status": Status.DRAFT,
    }
    fields.update(overrides)
    return Subject.objects.create(**fields)


class SubjectFormTests(TestCase):
    def test_blank_slug_is_generated_from_the_title(self):
        form = SubjectForm(data=VALID)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().slug, "retrieval-augmented-generation")

    def test_generated_slug_does_not_collide(self):
        make_subject(slug="retrieval-augmented-generation")
        form = SubjectForm(data=VALID)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().slug, "retrieval-augmented-generation-2")

    def test_hand_typed_duplicate_slug_is_rejected(self):
        make_subject(slug="taken")
        form = SubjectForm(data={**VALID, "slug": "taken"})
        self.assertFalse(form.is_valid())
        self.assertIn("slug", form.errors)

    def test_what_you_can_build_normalises_line_endings(self):
        form = SubjectForm(data={**VALID, "what_you_can_build": "One thing\r\n\r\n  Another  \r\n"})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["what_you_can_build"], "One thing\nAnother")

    def test_what_you_can_build_needs_two_items(self):
        form = SubjectForm(data={**VALID, "what_you_can_build": "Only one thing"})
        self.assertFalse(form.is_valid())
        self.assertIn("what_you_can_build", form.errors)

    def test_what_you_can_build_rejects_bullets(self):
        form = SubjectForm(data={**VALID, "what_you_can_build": "- One thing\n- Another thing"})
        self.assertFalse(form.is_valid())
        self.assertIn("what_you_can_build", form.errors)

    def test_editing_keeps_its_own_slug(self):
        subject = make_subject(slug="kept")
        form = SubjectForm(data={**VALID, "slug": "kept"}, instance=subject)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().slug, "kept")

    def test_date_note_is_optional(self):
        # VALID omits it entirely: most entries have an exact date and nothing to explain.
        form = SubjectForm(data=VALID)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().date_note, "")

    def test_date_note_round_trips(self):
        note = "No launch day — dated to the release that made it practical."
        form = SubjectForm(data={**VALID, "date_note": note})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().date_note, note)


class SeedDataTests(TestCase):
    """The seeds are hand-written, so only a test stops an uncited date going back in."""

    def test_every_entry_cites_a_source_and_a_parseable_date(self):
        for item in SUBJECTS:
            with self.subTest(slug=item["slug"]):
                self.assertTrue(item.get("source_url"), "no source_url")
                self.assertTrue(item.get("became_usable_on"), "no became_usable_on")
                date.fromisoformat(item["became_usable_on"])

    def test_reseeding_keeps_the_first_published_on(self):
        # published_on belongs in create_defaults only: re-running the seeder to pick up
        # edited copy must not restamp rows that were published months ago.
        call_command("seed_syllabus", stdout=StringIO())
        first = Subject.objects.get(slug="rag").published_on
        call_command("seed_syllabus", stdout=StringIO())
        self.assertEqual(Subject.objects.get(slug="rag").published_on, first)

    def test_reseeding_updates_edited_copy(self):
        call_command("seed_syllabus", stdout=StringIO())
        Subject.objects.filter(slug="rag").update(one_liner="stale")
        call_command("seed_syllabus", stdout=StringIO())
        self.assertNotEqual(Subject.objects.get(slug="rag").one_liner, "stale")


class AccessTests(TestCase):
    def test_anonymous_is_sent_to_login(self):
        response = self.client.get(reverse("cms:subjects"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/"))

    def test_signed_in_non_superuser_gets_403_not_a_login_loop(self):
        User.objects.create_user(username="reader", password="pw")
        self.client.login(username="reader", password="pw")
        self.assertEqual(self.client.get(reverse("cms:subjects")).status_code, 403)


class CMSTests(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="boss", email="boss@example.com", password="pw")
        self.client.login(username="boss", password="pw")

    def test_every_page_renders(self):
        make_subject()
        for name in ["cms:dashboard", "cms:subjects", "cms:queue", "cms:research", "cms:editorial"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_list_filters_by_status_category_and_search(self):
        make_subject(slug="a", title="Alpha", status=Status.PUBLISHED, category=Category.AGENTS)
        make_subject(slug="b", title="Beta", status=Status.DRAFT, category=Category.MEDIA)

        def slugs(query):
            page = self.client.get(reverse("cms:subjects"), query).context["page_obj"]
            return [subject.slug for subject in page.object_list]

        self.assertEqual(slugs({"status": "published"}), ["a"])
        self.assertEqual(slugs({"category": "media"}), ["b"])
        self.assertEqual(slugs({"q": "alph"}), ["a"])
        self.assertEqual(sorted(slugs({"status": "nonsense"})), ["a", "b"])

    def test_create_redirects_to_the_generated_slug(self):
        response = self.client.post(reverse("cms:subject_new"), VALID)
        self.assertRedirects(
            response,
            reverse("cms:subject_edit", kwargs={"slug": "retrieval-augmented-generation"}),
        )
        self.assertEqual(Subject.objects.get().status, Status.DRAFT)

    def test_invalid_create_saves_nothing(self):
        response = self.client.post(
            reverse("cms:subject_new"), {**VALID, "what_you_can_build": "one line"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subject.objects.exists())

    def test_publish_then_unpublish_keeps_the_first_published_on(self):
        subject = make_subject(slug="pub")
        url = reverse("cms:subject_publish", kwargs={"slug": "pub"})

        self.client.post(url, {"action": "publish"})
        subject.refresh_from_db()
        self.assertEqual(subject.status, Status.PUBLISHED)
        first_published = subject.published_on
        self.assertIsNotNone(first_published)

        self.client.post(url, {"action": "unpublish"})
        subject.refresh_from_db()
        self.assertEqual(subject.status, Status.DRAFT)
        self.assertEqual(subject.published_on, first_published)

        self.client.post(url, {"action": "publish"})
        subject.refresh_from_db()
        self.assertEqual(subject.published_on, first_published)

    def test_publish_returns_to_the_filtered_list(self):
        make_subject(slug="pub")
        response = self.client.post(
            reverse("cms:subject_publish", kwargs={"slug": "pub"}),
            {"action": "publish", "next": "/dashboard/subjects/?status=draft"},
        )
        self.assertRedirects(response, "/dashboard/subjects/?status=draft")

    def test_publish_ignores_an_offsite_next(self):
        make_subject(slug="pub")
        response = self.client.post(
            reverse("cms:subject_publish", kwargs={"slug": "pub"}),
            {"action": "publish", "next": "https://evil.example.com/"},
        )
        self.assertRedirects(response, reverse("cms:subject_edit", kwargs={"slug": "pub"}))

    def test_unknown_slug_is_404(self):
        self.assertEqual(
            self.client.get(reverse("cms:subject_edit", kwargs={"slug": "nope"})).status_code, 404
        )


def model_verdict(**overrides):
    data = {
        "is_new_subject": True,
        "duplicate_of_slug": None,
        "reason": "Nothing could drive a desktop app from a sentence before.",
        "title": "Computer use",
        "slug": "computer-use",
        "one_liner": "A model that works your screen with a mouse and keyboard.",
        "what_you_can_build": "Fill a web form from a spreadsheet\nFile expenses in an old portal",
        "before_this": "You clicked through it yourself.",
        "why_new": "Automation needed an API the app never had.",
        "category": "agents",
        "became_usable_on": "2024-10-22",
        "date_note": "",
        "source_url": "https://example.com/launch",
        "resource_url": "https://example.com/docs",
        "sources": ["https://example.com/launch"],
    }
    data.update(overrides)
    return data


def model_response(data=None, status="completed"):
    """The shape judge.parse walks: reasoning and search items first, then the message."""
    content = [SimpleNamespace(type="output_text", text=json.dumps(data))] if data else []
    return SimpleNamespace(
        id="resp_1",
        status=status,
        error=SimpleNamespace(message="boom") if status == "failed" else None,
        incomplete_details=None,
        output=[
            SimpleNamespace(type="web_search_call"),
            SimpleNamespace(type="message", content=content),
        ],
    )


def fake_client(retrieved=None):
    client = MagicMock()
    client.responses.create.return_value = SimpleNamespace(id="resp_1")
    client.responses.retrieve.return_value = retrieved
    return client


class ResearchTests(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="boss", email="boss@example.com", password="pw")
        self.client.login(username="boss", password="pw")

    def running(self):
        return TopicResearch.objects.create(topic="computer use", response_id="resp_1")

    def detail(self, research):
        return self.client.get(reverse("cms:research_detail", kwargs={"pk": research.pk}))

    @override_settings(OPENAI_API_KEY="")
    def test_without_a_key_nothing_is_saved(self):
        response = self.client.post(reverse("cms:research"), {"topic": "computer use"})
        self.assertContains(response, "OPENAI_API_KEY")
        self.assertFalse(TopicResearch.objects.exists())

    def test_post_starts_a_background_web_search(self):
        client = fake_client()
        with patch("syllabus.judge.get_client", return_value=client):
            response = self.client.post(reverse("cms:research"), {"topic": "computer use"})

        research = TopicResearch.objects.get()
        self.assertRedirects(
            response,
            reverse("cms:research_detail", kwargs={"pk": research.pk}),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            (research.status, research.response_id), (ResearchStatus.RUNNING, "resp_1")
        )
        kwargs = client.responses.create.call_args.kwargs
        self.assertTrue(kwargs["background"])
        self.assertEqual(kwargs["tools"], [{"type": "web_search"}])

    def test_page_reloads_only_while_running(self):
        research = self.running()
        with patch(
            "syllabus.judge.get_client",
            return_value=fake_client(model_response(status="in_progress")),
        ):
            self.assertContains(self.detail(research), 'http-equiv="refresh"')
        with patch(
            "syllabus.judge.get_client", return_value=fake_client(model_response(model_verdict()))
        ):
            self.assertNotContains(self.detail(research), 'http-equiv="refresh"')

    def test_accepted_files_exactly_one_dated_draft(self):
        research = self.running()
        with patch(
            "syllabus.judge.get_client", return_value=fake_client(model_response(model_verdict()))
        ):
            self.detail(research)
            self.detail(research)
            self.client.get(reverse("cms:research"))

        research.refresh_from_db()
        self.assertEqual(research.verdict, Verdict.ACCEPTED)
        subject = Subject.objects.get()
        self.assertEqual(research.subject, subject)
        self.assertEqual(subject.status, Status.DRAFT)
        self.assertEqual(subject.became_usable_on, date(2024, 10, 22))
        self.assertEqual(subject.source_url, "https://example.com/launch")

    def test_rejected_files_nothing_until_drafted_anyway(self):
        research = self.running()
        rejected = model_verdict(is_new_subject=False, reason="A nicer version of scripting.")
        with patch("syllabus.judge.get_client", return_value=fake_client(model_response(rejected))):
            self.assertContains(self.detail(research), "Draft anyway")
        self.assertFalse(Subject.objects.exists())

        url = reverse("cms:research_draft", kwargs={"pk": research.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("cms:subject_edit", kwargs={"slug": "computer-use"}))
        self.client.post(url)
        self.assertEqual(Subject.objects.count(), 1)
        research.refresh_from_db()
        self.assertEqual(research.verdict, Verdict.REJECTED_LLM)  # the model's call stands

    def test_unsafe_model_urls_are_dropped(self):
        research = self.running()
        data = model_verdict(
            resource_url="javascript:alert(1)",
            sources=["javascript:alert(1)", "https://ok.example.com/"],
        )
        with patch("syllabus.judge.get_client", return_value=fake_client(model_response(data))):
            self.detail(research)

        research.refresh_from_db()
        self.assertEqual(research.result["sources"], ["https://ok.example.com/"])
        self.assertEqual(Subject.objects.get().resource_url, "")

    def test_a_failed_run_is_recorded(self):
        research = self.running()
        with patch(
            "syllabus.judge.get_client", return_value=fake_client(model_response(status="failed"))
        ):
            self.assertContains(self.detail(research), "boom")
        research.refresh_from_db()
        self.assertEqual(research.status, ResearchStatus.FAILED)


class CrawlJudgeTests(TestCase):
    """The crawler shares judge.py with research; this pins its accept path."""

    def test_accepted_story_becomes_a_draft_sourced_to_the_story(self):
        story = {
            "hn_id": "1",
            "title": "Computer use",
            "url": "https://example.com/hn",
            "points": 99,
        }
        payload = {k: v for k, v in model_verdict().items() if k != "became_usable_on"}
        client = fake_client()
        client.responses.create.return_value = model_response(payload)

        subject = CrawlCommand(stdout=StringIO()).judge(client, story, index="")

        self.assertEqual(subject.source_url, "https://example.com/hn")
        self.assertIsNone(subject.became_usable_on)
        self.assertEqual(CrawlCandidate.objects.get().verdict, Verdict.ACCEPTED)


class EditorialAPITests(TestCase):
    """The /about page reads the bar over this endpoint, signed out."""

    def test_anonymous_gets_the_bar(self):
        response = self.client.get(reverse("api-v1-editorial"))
        self.assertEqual(response.status_code, 200)

        body = response.json()
        self.assertTrue(body["bar"])
        self.assertTrue(body["qualifies"])
        self.assertTrue(body["disqualifies"])
        self.assertEqual(len(body["categories"]), len(Category.choices))
        self.assertEqual([q["question"] for q in body["three_questions"]][:1], ["What is it?"])

    def test_every_category_carries_a_note(self):
        # A new Category member with no CATEGORY_NOTES entry would render a blank line
        # on /about rather than fail anywhere, so assert the pairing here.
        for category in self.client.get(reverse("api-v1-editorial")).json()["categories"]:
            self.assertTrue(category["note"], category["slug"])
