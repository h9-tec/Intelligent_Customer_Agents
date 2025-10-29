from __future__ import annotations

from django.contrib import admin

from .models import Category, Product, ProductDescription, ProductName


class ProductNameInline(admin.TabularInline):
    model = ProductName
    extra = 1


class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "brand", "is_active")
    list_filter = ("brand", "is_active")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "brand",
        "category",
        "base_price",
        "stock",
        "is_active",
        "manufacturer",
        "model_number",
        "release_year",
    )
    list_filter = ("brand", "category", "is_active", "release_year")
    search_fields = ("sku", "manufacturer", "model_number")
    inlines = [ProductNameInline, ProductDescriptionInline]


