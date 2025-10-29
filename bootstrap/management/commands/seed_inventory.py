from __future__ import annotations

from decimal import Decimal

from django.core.management.base import BaseCommand

from brandkit.models import BrandProfile
from inventory.models import Category, Product, ProductDescription, ProductName


class Command(BaseCommand):
    help = "Seed inventory with sample electronics."

    def handle(self, *args, **options):  # type: ignore[override]
        brand, _ = BrandProfile.objects.get_or_create(name="ElectroMart")
        phones, _ = Category.objects.get_or_create(name="Phones", brand=brand)
        laptops, _ = Category.objects.get_or_create(name="Laptops", brand=brand)
        accessories, _ = Category.objects.get_or_create(name="Accessories", brand=brand)

        def add_product(sku: str, name: str, price: Decimal, category: Category, specs: dict):
            p, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    "brand": brand,
                    "base_price": price,
                    "category": category,
                    "stock": 100,
                    "is_active": True,
                    "manufacturer": specs.get("manufacturer", brand.name),
                    "model_number": specs.get("model", sku),
                    "release_year": specs.get("year", 2024),
                    "specifications": specs,
                },
            )
            ProductName.objects.update_or_create(product=p, language="en", defaults={"name": name})
            ProductDescription.objects.update_or_create(
                product=p,
                language="en",
                defaults={"description": f"{name} specs: {specs}"},
            )

        add_product("PHN-001", "Electro One", Decimal("499.00"), phones, {"ram": "6GB", "storage": "128GB"})
        add_product("LPT-001", "ElectroBook 13", Decimal("999.00"), laptops, {"ram": "16GB", "ssd": "512GB"})
        add_product("ACC-001", "USB-C Charger", Decimal("29.00"), accessories, {"watt": "30W"})

        self.stdout.write(self.style.SUCCESS("Seeded inventory."))


