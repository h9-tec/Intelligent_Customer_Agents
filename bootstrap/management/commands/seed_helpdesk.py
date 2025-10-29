from __future__ import annotations

from django.core.management.base import BaseCommand

from helpdesk.models import Faq


class Command(BaseCommand):
    help = "Seed helpdesk FAQs."

    def handle(self, *args, **options):  # type: ignore[override]
        Faq.objects.get_or_create(
            question="What is the warranty period for phones?",
            defaults={"answer": "All phones include a 12-month warranty.", "language": "en", "category": "warranty"},
        )
        Faq.objects.get_or_create(
            question="هل الشاحن متوافق مع جميع الهواتف؟",
            defaults={"answer": "متوافق مع الأجهزة التي تدعم USB-C.", "language": "ar", "category": "compatibility"},
        )
        self.stdout.write(self.style.SUCCESS("Seeded helpdesk."))


