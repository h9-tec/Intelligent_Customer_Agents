from __future__ import annotations

from decimal import Decimal

from django.core.management.base import BaseCommand

from orders.models import ShippingOption
from payments.models import PaymentOptions


class Command(BaseCommand):
    help = "Seed orders-related options."

    def handle(self, *args, **options):  # type: ignore[override]
        ShippingOption.objects.get_or_create(name="Standard", defaults={"price": Decimal("5.00"), "estimated_days": 5})
        ShippingOption.objects.get_or_create(name="Express", defaults={"price": Decimal("15.00"), "estimated_days": 2})
        PaymentOptions.objects.get_or_create(name="Cash on Delivery", defaults={"price": Decimal("0.00")})
        PaymentOptions.objects.get_or_create(name="Credit Card", defaults={"price": Decimal("2.50")})
        self.stdout.write(self.style.SUCCESS("Seeded orders/payment options."))


