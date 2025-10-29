from __future__ import annotations

from django.contrib import admin

from .models import ProductEmbedding, Recommendation, RecommendationProduct


@admin.register(ProductEmbedding)
class ProductEmbeddingAdmin(admin.ModelAdmin):
    list_display = ("product", "language", "created_at")
    search_fields = ("product__sku", "product__names__name")
    list_filter = ("language",)


class RecommendationProductInline(admin.TabularInline):
    model = RecommendationProduct
    extra = 0


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    inlines = [RecommendationProductInline]


