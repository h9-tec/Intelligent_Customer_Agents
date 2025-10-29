from __future__ import annotations

from django.db import models


class Customer(models.Model):
    phone = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone"], name="idx_customer_phone"),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name or self.phone}"


def get_or_create_customer_by_phone(phone: str, defaults: dict | None = None) -> Customer:
    defaults = defaults or {}
    customer, _ = Customer.objects.get_or_create(phone=phone, defaults=defaults)
    return customer


def update_customer_info(customer: Customer, **kwargs) -> Customer:
    for key, value in kwargs.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    customer.save(update_fields=[k for k in kwargs.keys() if hasattr(customer, k)])
    return customer


