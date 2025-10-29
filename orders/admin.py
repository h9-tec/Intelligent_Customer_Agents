from __future__ import annotations

from django.contrib import admin

from .models import Cart, CartItem, Order, OrderUpdateRequest, ShippingOption


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("customer__phone", "customer__name")
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer", "status", "total_price", "created_at", "completed_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "customer__phone", "customer__name")


@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "estimated_days", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(OrderUpdateRequest)
class OrderUpdateRequestAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "requested_at")
    list_filter = ("status", "requested_at")


