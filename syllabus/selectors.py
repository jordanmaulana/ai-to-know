"""Read queries behind the CMS dashboard. Kept out of views so they stay testable."""

from datetime import timedelta

from django.db.models import Count, Max, Q
from django.utils import timezone

from syllabus.models import Category, CrawlCandidate, Status, Subject, Verdict


def subject_totals():
    return Subject.objects.aggregate(
        total=Count("id"),
        published=Count("id", filter=Q(status=Status.PUBLISHED)),
        drafts=Count("id", filter=Q(status=Status.DRAFT)),
        undated=Count("id", filter=Q(became_usable_on__isnull=True)),
    )


def subjects_by_category():
    """One row per category, including the empty ones.

    values()+annotate() only returns categories that have rows, so the list is driven by
    Category.choices and filled in from the query.
    """
    rows = {
        row["category"]: row
        for row in Subject.objects.values("category").annotate(
            total=Count("id"),
            published=Count("id", filter=Q(status=Status.PUBLISHED)),
        )
    }
    return [
        {
            "value": value,
            "label": label,
            "total": rows.get(value, {}).get("total", 0),
            "published": rows.get(value, {}).get("published", 0),
        }
        for value, label in Category.choices
    ]


def recent_drafts(limit=8):
    # Newest-filed first, not Meta.ordering: crawler drafts have became_usable_on=None, which
    # sorts last on SQLite and first on Postgres.
    return Subject.objects.filter(status=Status.DRAFT).order_by("-created_on", "id")[:limit]


def recent_candidates(limit=8):
    return CrawlCandidate.objects.select_related("subject").order_by("-created_on", "id")[:limit]


def crawl_snapshot(hours=24):
    """A rolling window over crawl candidates.

    Deliberately not "the last run": there is no CrawlRun model, no run id, and record() uses
    update_or_create, so a re-seen story bumps updated_on rather than created_on. Clustering
    rows into runs would look authoritative and be wrong the first time two runs land close
    together.
    """
    since = timezone.now() - timedelta(hours=hours)
    snapshot = CrawlCandidate.objects.filter(created_on__gte=since).aggregate(
        seen=Count("id"),
        accepted=Count("id", filter=Q(verdict=Verdict.ACCEPTED)),
        rejected=Count("id", filter=Q(verdict=Verdict.REJECTED_LLM)),
        duplicate=Count("id", filter=Q(verdict=Verdict.DUPLICATE)),
        skipped=Count("id", filter=Q(verdict=Verdict.SKIPPED_HEURISTIC)),
    )
    snapshot["last_seen"] = CrawlCandidate.objects.aggregate(at=Max("created_on"))["at"]
    snapshot["window_hours"] = hours
    return snapshot
