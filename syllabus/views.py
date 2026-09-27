"""The superadmin CMS: everything you need to run the syllabus without touching /admin/.

Server-rendered, no JavaScript. Filtering, search and pagination are plain querystrings, so
every view of the list is a URL you can bookmark or paste to someone else.
"""

import logging

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from core.views import SuperuserRequiredMixin
from syllabus import editorial, judge, selectors
from syllabus.forms import SubjectForm, TopicForm
from syllabus.models import (
    Category,
    CrawlCandidate,
    ResearchStatus,
    Status,
    Subject,
    TopicResearch,
    Verdict,
)

logger = logging.getLogger(__name__)

SUBJECTS_PER_PAGE = 25
CANDIDATES_PER_PAGE = 50
RESEARCH_PER_PAGE = 25

SORTS = {
    "edited": "Recently edited",
    "usable": "Newest capability",
    "title": "Title",
}


class DashboardView(SuperuserRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "cms/dashboard.html",
            {
                "totals": selectors.subject_totals(),
                "by_category": selectors.subjects_by_category(),
                "drafts": selectors.recent_drafts(8),
                "candidates": selectors.recent_candidates(8),
                "crawl": selectors.crawl_snapshot(),
            },
        )


class SubjectListView(SuperuserRequiredMixin, View):
    def get(self, request):
        status = request.GET.get("status") or ""
        category = request.GET.get("category") or ""
        q = (request.GET.get("q") or "").strip()
        sort = request.GET.get("sort") or "edited"

        subjects = Subject.objects.all()
        if status in Status.values:
            subjects = subjects.filter(status=status)
        if category in Category.values:
            subjects = subjects.filter(category=category)
        if q:
            # Mirrors syllabus_api.py, plus slug because that is how you look up a draft.
            subjects = subjects.filter(
                Q(title__icontains=q) | Q(one_liner__icontains=q) | Q(slug__icontains=q)
            )

        # "id" is the tiebreak: without it, equal sort keys shuffle rows between pages.
        if sort == "usable":
            subjects = subjects.order_by(F("became_usable_on").desc(nulls_last=True), "title", "id")
        elif sort == "title":
            subjects = subjects.order_by("title", "id")
        else:
            sort = "edited"
            subjects = subjects.order_by("-updated_on", "id")

        page = Paginator(subjects, SUBJECTS_PER_PAGE).get_page(request.GET.get("page"))
        return render(
            request,
            "cms/subject_list.html",
            {
                "page_obj": page,
                "statuses": Status.choices,
                "categories": Category.choices,
                "sorts": SORTS.items(),
                "status": status if status in Status.values else "",
                "category": category if category in Category.values else "",
                "q": q,
                "sort": sort,
                "filtered": bool(status or category or q),
            },
        )


class SubjectFormView(SuperuserRequiredMixin, View):
    """Create and edit in one view; `slug` in the URL is what tells them apart."""

    def get(self, request, slug=None):
        subject = get_object_or_404(Subject, slug=slug) if slug else None
        return self.render_form(request, SubjectForm(instance=subject), subject)

    def post(self, request, slug=None):
        subject = get_object_or_404(Subject, slug=slug) if slug else None
        form = SubjectForm(request.POST, instance=subject)
        if not form.is_valid():
            messages.error(request, "Nothing was saved — fix the errors below.")
            return self.render_form(request, form, subject)

        saved = form.save(commit=False)
        saved.actor = request.user
        saved.save()
        messages.success(request, f"Saved “{saved.title}”.")
        return redirect("cms:subject_edit", slug=saved.slug)

    def render_form(self, request, form, subject):
        return render(
            request,
            "cms/subject_form.html",
            {
                "form": form,
                "subject": subject,
                "public_url": f"{settings.FRONTEND_URL}/subjects/{subject.slug}" if subject else "",
            },
        )


class SubjectPublishView(SuperuserRequiredMixin, View):
    def post(self, request, slug):
        subject = get_object_or_404(Subject, slug=slug)
        action = request.POST.get("action")

        if action == "publish":
            subject.publish()
            messages.success(request, f"Published “{subject.title}” — it is live on the site.")
        elif action == "unpublish":
            subject.status = Status.DRAFT
            # instance.save(), not queryset.update(): auto_now is skipped unless updated_on is
            # named in update_fields, and the list's "edited" column reads it.
            subject.save(update_fields=["status", "updated_on"])
            messages.success(request, f"“{subject.title}” is back to draft.")
        else:
            messages.error(request, "Unknown action — nothing changed.")

        target = self.safe_next(request)
        if target:
            return redirect(target)
        return redirect("cms:subject_edit", slug=subject.slug)

    def safe_next(self, request):
        """Return to whatever filtered list the button was pressed on, if it is ours."""
        target = request.POST.get("next")
        if target and url_has_allowed_host_and_scheme(
            target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            return target
        return ""


class QueueView(SuperuserRequiredMixin, View):
    """Read-only, like CrawlCandidateAdmin — the crawler owns these rows."""

    def get(self, request):
        verdict = request.GET.get("verdict") or ""
        q = (request.GET.get("q") or "").strip()

        candidates = CrawlCandidate.objects.select_related("subject").order_by("-created_on", "id")
        if verdict in Verdict.values:
            candidates = candidates.filter(verdict=verdict)
        if q:
            candidates = candidates.filter(Q(hn_title__icontains=q) | Q(reason__icontains=q))

        page = Paginator(candidates, CANDIDATES_PER_PAGE).get_page(request.GET.get("page"))
        return render(
            request,
            "cms/queue.html",
            {
                "page_obj": page,
                "verdicts": Verdict.choices,
                "verdict": verdict if verdict in Verdict.values else "",
                "q": q,
                "filtered": bool(verdict or q),
                "crawl": selectors.crawl_snapshot(),
            },
        )


class EditorialView(SuperuserRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "cms/editorial.html",
            {
                "bar": editorial.BAR,
                "three_questions": editorial.THREE_QUESTIONS,
                "qualifies": editorial.QUALIFIES,
                "disqualifies": editorial.DISQUALIFIES,
                "rubric": editorial.RUBRIC,
                "research_rubric": editorial.RESEARCH_RUBRIC,
                "categories": [
                    (label, editorial.CATEGORY_NOTES.get(value, ""))
                    for value, label in Category.choices
                ],
            },
        )


def refresh_running(request, rows):
    """Collect any background research that has finished since the last page load."""
    client = judge.get_client()
    if client is None:
        return
    for research in rows:
        try:
            judge.refresh(research, client)
        except Exception:  # a flaky poll must not take the page down; the next load retries
            logger.exception("Failed to check on research %s", research.pk)
            messages.warning(request, f"Could not reach OpenAI about “{research.topic}”.")


class ResearchView(SuperuserRequiredMixin, View):
    """Type a topic, and the model searches the web and judges it against the bar."""

    def get(self, request):
        return self.render_page(request, TopicForm())

    def post(self, request):
        form = TopicForm(request.POST)
        if not form.is_valid():
            return self.render_page(request, form)

        client = judge.get_client()
        if client is None:
            messages.error(request, "OPENAI_API_KEY is not set, so nothing was researched.")
            return self.render_page(request, form)

        research = form.save(commit=False)
        research.actor = request.user
        try:
            research.response_id = judge.start(client, research.topic, research.url).id
        except Exception as exc:
            logger.exception("Failed to start research on %r", research.topic)
            research.status, research.error = ResearchStatus.FAILED, str(exc)
        research.save()
        return redirect("cms:research_detail", pk=research.pk)

    def render_page(self, request, form):
        refresh_running(request, TopicResearch.objects.filter(status=ResearchStatus.RUNNING))
        rows = TopicResearch.objects.select_related("subject").order_by("-created_on", "id")
        page = Paginator(rows, RESEARCH_PER_PAGE).get_page(request.GET.get("page"))
        return render(request, "cms/research.html", {"form": form, "page_obj": page})


class ResearchDetailView(SuperuserRequiredMixin, View):
    """Its own page so the auto-refresh while it runs cannot wipe a half-typed topic."""

    def get(self, request, pk):
        research = get_object_or_404(TopicResearch.objects.select_related("subject"), pk=pk)
        if research.status == ResearchStatus.RUNNING:
            refresh_running(request, [research])
            research.refresh_from_db()
        return render(request, "cms/research_detail.html", {"research": research})


class ResearchDraftView(SuperuserRequiredMixin, View):
    """Overrule the model: file its copy as a draft whatever the verdict was."""

    def post(self, request, pk):
        with transaction.atomic():
            research = get_object_or_404(
                TopicResearch.objects.select_for_update(), pk=pk, status=ResearchStatus.DONE
            )
            if research.subject is None:
                if not research.result.get("title"):
                    messages.error(request, "The model wrote no copy for this one.")
                    return redirect("cms:research_detail", pk=pk)
                research.subject = judge.create_draft(research.result, judge.draft_source(research))
                research.save(update_fields=["subject", "updated_on"])
                messages.success(request, f"Filed “{research.subject.title}” as a draft.")
        return redirect("cms:subject_edit", slug=research.subject.slug)
