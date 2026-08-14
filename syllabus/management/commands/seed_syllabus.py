from datetime import date

from django.core.management.base import BaseCommand
from django.utils import timezone

from syllabus.models import Status, Subject
from syllabus.seed_data import SUBJECTS


class Command(BaseCommand):
    help = "Load the hand-written syllabus subjects. Idempotent: safe to re-run."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete the seeded subjects instead of loading them.",
        )

    def handle(self, *args, **options):
        slugs = [item["slug"] for item in SUBJECTS]

        if options["reset"]:
            deleted, _ = Subject.objects.filter(slug__in=slugs).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} seeded row(s)."))
            return

        created = updated = 0
        now = timezone.now()

        for item in SUBJECTS:
            payload = dict(item)
            slug = payload.pop("slug")
            usable_on = payload.pop("became_usable_on", None)
            payload["became_usable_on"] = date.fromisoformat(usable_on) if usable_on else None
            payload["status"] = Status.PUBLISHED

            # published_on lives in create_defaults only, so re-running the seeder to pick up
            # edited copy does not restamp rows that were published months ago.
            subject, was_created = Subject.objects.update_or_create(
                slug=slug,
                defaults=payload,
                create_defaults={**payload, "published_on": now},
            )
            if not was_created:
                updated += 1
            else:
                created += 1
            self.stdout.write(f"  {'+' if was_created else '~'} {subject.slug}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(SUBJECTS)} subjects ({created} new, {updated} updated)."
            )
        )
