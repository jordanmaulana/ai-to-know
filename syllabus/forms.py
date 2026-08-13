from django import forms
from django.utils.text import slugify

from syllabus.models import Subject

# No widget_tweaks in this project, so the Tailwind classes live with the widgets.
INPUT = (
    "w-full rounded-md border border-rule bg-card px-3 py-2 text-sm text-ink "
    "placeholder:text-muted focus:border-accent focus:ring-2 focus:ring-accent/20 "
    "focus:outline-none"
)
AREA = INPUT + " min-h-28 leading-relaxed"

BULLET_CHARS = "-*•–—"


class SubjectForm(forms.ModelForm):
    """Everything about a subject except its publication state.

    status/published_on are handled by SubjectPublishView so Subject.publish()'s stamp-once
    semantics cannot be sidestepped by flipping a select.
    """

    class Meta:
        model = Subject
        fields = [
            "title",
            "slug",
            "category",
            "became_usable_on",
            "one_liner",
            "what_you_can_build",
            "before_this",
            "why_new",
            "resource_url",
            "source_url",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT, "autofocus": True}),
            "slug": forms.TextInput(
                attrs={"class": INPUT, "placeholder": "leave blank to generate from the title"}
            ),
            "category": forms.Select(attrs={"class": INPUT}),
            # format= is required: without it the stored date renders localised ("Jan. 5, 2024")
            # and <input type="date"> silently shows empty when editing.
            "became_usable_on": forms.DateInput(
                attrs={"class": INPUT, "type": "date"}, format="%Y-%m-%d"
            ),
            "one_liner": forms.TextInput(attrs={"class": INPUT}),
            "what_you_can_build": forms.Textarea(attrs={"class": AREA, "rows": 5}),
            "before_this": forms.Textarea(attrs={"class": AREA, "rows": 4}),
            "why_new": forms.Textarea(attrs={"class": AREA, "rows": 4}),
            "resource_url": forms.URLInput(attrs={"class": INPUT}),
            "source_url": forms.URLInput(attrs={"class": INPUT}),
        }
        labels = {
            "one_liner": "What is it",
            "what_you_can_build": "What you can make",
            "before_this": "Before this",
            "why_new": "Why it is new",
            "became_usable_on": "Became usable on",
            "resource_url": "Start here URL",
            "source_url": "Source URL",
        }
        help_texts = {
            "slug": "The public URL: /subjects/<slug>. Changing it breaks existing links.",
            "one_liner": "One plain sentence. No hype.",
            "what_you_can_build": "One concrete thing per line, no bullet characters.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False

    def clean_what_you_can_build(self):
        raw = self.cleaned_data["what_you_can_build"]
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if len(lines) < 2:
            raise forms.ValidationError("At least two concrete things, one per line.")
        if any(line[0] in BULLET_CHARS for line in lines):
            raise forms.ValidationError(
                "No bullet characters — one plain item per line, the site adds the dots."
            )
        return "\n".join(lines)  # also normalises the CRLF a textarea posts

    def clean(self):
        # Slug generation belongs here, not in clean_slug(): per-field cleaning runs in
        # Meta.fields order, so clean_slug() cannot rely on title being cleaned yet.
        cleaned = super().clean()
        if not cleaned.get("slug") and cleaned.get("title"):
            cleaned["slug"] = self._unique_slug(slugify(cleaned["title"])[:60] or "untitled")
        return cleaned

    def _unique_slug(self, base):
        """Same -N dedupe the crawler uses in crawl_hn.create_draft."""
        taken = Subject.objects.all()
        if self.instance.pk:
            taken = taken.exclude(pk=self.instance.pk)
        slug, n = base, 2
        while taken.filter(slug=slug).exists():
            slug, n = f"{base[:57]}-{n}", n + 1
        return slug
