from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from syllabus.forms import SubjectForm
from syllabus.models import Category, Status, Subject

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
        for name in ["cms:dashboard", "cms:subjects", "cms:queue", "cms:editorial"]:
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
