from django.db import models
from django.utils import timezone

from core.models import BaseModel


class Category(models.TextChoices):
    BUILD = "build", "Build software"
    AUTOMATE = "automate", "Automate work"
    AGENTS = "agents", "Agents"
    MEDIA = "media", "Media"
    INTERFACE = "interface", "Interfaces"
    INFRA = "infra", "Infrastructure"


class Status(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class Subject(BaseModel):
    """One syllabus entry: what it is, what it unlocks, and how people coped before."""

    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=160)
    one_liner = models.CharField(max_length=300)
    what_you_can_build = models.TextField(help_text="One concrete thing per line.")
    before_this = models.TextField(help_text="How people did this before it existed.")
    why_new = models.TextField(help_text="What was impossible or impractical before.")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.BUILD)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    resource_url = models.URLField(blank=True, default="")
    source_url = models.URLField(blank=True, default="")
    became_usable_on = models.DateField(
        null=True, blank=True, help_text="Roughly when this became practical for normal people."
    )
    date_note = models.CharField(
        max_length=300,
        blank=True,
        default="",
        help_text="Why this date and not another. Fill in when it is an editorial anchor.",
    )
    published_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-became_usable_on", "title"]
        indexes = [models.Index(fields=["status", "category"])]

    def __str__(self):
        return self.title

    def publish(self):
        self.status = Status.PUBLISHED
        if not self.published_on:
            self.published_on = timezone.now()
        self.save(update_fields=["status", "published_on", "updated_on"])


class Verdict(models.TextChoices):
    SKIPPED_HEURISTIC = "skipped_heuristic", "Skipped (heuristic)"
    REJECTED_LLM = "rejected_llm", "Rejected (model)"
    DUPLICATE = "duplicate", "Duplicate"
    ACCEPTED = "accepted", "Accepted"


class CrawlCandidate(BaseModel):
    """One Hacker News story the crawler has already looked at.

    `hn_id` is unique so a story is never fetched, judged, or paid for twice.
    """

    hn_id = models.CharField(max_length=32, unique=True)
    hn_title = models.CharField(max_length=500)
    hn_url = models.URLField(blank=True, default="")
    points = models.IntegerField(default=0)
    verdict = models.CharField(max_length=32, choices=Verdict.choices)
    reason = models.TextField(blank=True, default="")
    subject = models.ForeignKey(
        Subject, null=True, blank=True, on_delete=models.SET_NULL, related_name="candidates"
    )

    class Meta:
        ordering = ["-created_on"]
        indexes = [models.Index(fields=["verdict"])]

    def __str__(self):
        return f"{self.hn_title} ({self.verdict})"
