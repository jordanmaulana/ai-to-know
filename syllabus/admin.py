from django.contrib import admin
from django.utils import timezone

from syllabus.models import CrawlCandidate, Status, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "became_usable_on", "updated_on")
    list_filter = ("status", "category")
    search_fields = ("title", "slug", "one_liner", "why_new")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_on", "updated_on", "published_on")
    actions = ("publish_subjects", "unpublish_subjects")
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "status", "became_usable_on")}),
        ("Content", {"fields": ("one_liner", "what_you_can_build", "before_this", "why_new")}),
        ("Links", {"fields": ("resource_url", "source_url")}),
        ("Meta", {"fields": ("created_on", "updated_on", "published_on")}),
    )

    @admin.action(description="Publish selected subjects")
    def publish_subjects(self, request, queryset):
        now = timezone.now()
        count = 0
        for subject in queryset:
            subject.status = Status.PUBLISHED
            subject.published_on = subject.published_on or now
            subject.save(update_fields=["status", "published_on", "updated_on"])
            count += 1
        self.message_user(request, f"Published {count} subject(s).")

    @admin.action(description="Move selected subjects back to draft")
    def unpublish_subjects(self, request, queryset):
        # Row-by-row, not queryset.update(): update() skips auto_now, which would leave
        # updated_on stale and make the CMS "edited" column lie.
        count = 0
        for subject in queryset:
            subject.status = Status.DRAFT
            subject.save(update_fields=["status", "updated_on"])
            count += 1
        self.message_user(request, f"Moved {count} subject(s) back to draft.")


@admin.register(CrawlCandidate)
class CrawlCandidateAdmin(admin.ModelAdmin):
    list_display = ("hn_title", "verdict", "points", "subject", "created_on")
    list_filter = ("verdict",)
    search_fields = ("hn_title", "hn_id", "reason")
    readonly_fields = (
        "hn_id",
        "hn_title",
        "hn_url",
        "points",
        "verdict",
        "reason",
        "subject",
        "created_on",
        "updated_on",
    )

    def has_add_permission(self, request):
        return False
