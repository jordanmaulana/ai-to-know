"""The superadmin CMS: everything you need to run the syllabus without touching /admin/.

Server-rendered, no JavaScript. Filtering, search and pagination are plain querystrings, so
every view of the list is a URL you can bookmark or paste to someone else.
"""

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from core.views import SuperuserRequiredMixin
from syllabus import editorial, selectors
from syllabus.forms import SubjectForm
from syllabus.models import Category, CrawlCandidate, Status, Subject, Verdict

SUBJECTS_PER_PAGE = 25
CANDIDATES_PER_PAGE = 50

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
            subjects = subjects.order_by(
                F("became_usable_on").desc(nulls_last=True), "title", "id"
            )
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
                "public_url": f"{settings.FRONTEND_URL}/subjects/{subject.slug}"
                if subject
                else "",
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

        candidates = CrawlCandidate.objects.select_related("subject").order_by(
            "-created_on", "id"
        )
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
                "categories": [
                    (label, editorial.CATEGORY_NOTES.get(value, ""))
                    for value, label in Category.choices
                ],
            },
        )
