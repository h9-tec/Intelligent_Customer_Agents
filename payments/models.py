from __future__ import annotations

from decimal import Decimal

from django.db import models

from orders.models import Order
from users.models import Customer


class PaymentOptions(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_option = models.ForeignKey(PaymentOptions, on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Payment {self.id} - {self.status}"

    # Placeholder hooks for gateway integration
    def capture(self) -> None:  # pragma: no cover
        pass

    def refund(self) -> None:  # pragma: no cover
        pass


