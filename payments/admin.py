from __future__ import annotations

from django.contrib import admin

from .models import Payment, PaymentOptions


@admin.register(PaymentOptions)
class PaymentOptionsAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "customer", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order__order_number", "customer__phone", "transaction_id")


