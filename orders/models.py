from __future__ import annotations

from decimal import Decimal

from django.db import models

from inventory.models import Product
from users.models import Customer


class ShippingOption(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Cart {self.pk} for {self.customer}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    order_number = models.CharField(max_length=32, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")
    cart = models.OneToOneField(Cart, on_delete=models.PROTECT, related_name="order")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.PROTECT, null=True, blank=True)
    payment_option = models.ForeignKey("payments.PaymentOptions", on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["order_number"], name="idx_orders_number"),
        ]


class OrderUpdateRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="update_requests")
    status = models.CharField(max_length=16, choices=Order.Status.choices)
    requested_at = models.DateTimeField(auto_now_add=True)


