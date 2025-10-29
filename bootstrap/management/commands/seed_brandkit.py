from __future__ import annotations

from django.core.management.base import BaseCommand

from brandkit.models import BrandFeature, BrandProfile, BrandTaxonomy


class Command(BaseCommand):
    help = "Seed brandkit with a sample brand."

    def handle(self, *args, **options):  # type: ignore[override]
        brand, _ = BrandProfile.objects.get_or_create(name="ElectroMart", defaults={"language_default": "en"})
        BrandFeature.objects.get_or_create(brand=brand, feature_name="recommendations", defaults={"is_active": True})
        BrandTaxonomy.objects.get_or_create(brand=brand, category="Phones")
        BrandTaxonomy.objects.get_or_create(brand=brand, category="Laptops")
        BrandTaxonomy.objects.get_or_create(brand=brand, category="Accessories")
        self.stdout.write(self.style.SUCCESS("Seeded brandkit."))


