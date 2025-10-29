from __future__ import annotations

from django.contrib import admin

from .models import BrandFeature, BrandProfile, BrandTaxonomy


class BrandFeatureInline(admin.TabularInline):
    model = BrandFeature
    extra = 0


class BrandTaxonomyInline(admin.TabularInline):
    model = BrandTaxonomy
    extra = 0


@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "language_default")
    search_fields = ("name",)
    inlines = [BrandFeatureInline, BrandTaxonomyInline]


@admin.register(BrandTaxonomy)
class BrandTaxonomyAdmin(admin.ModelAdmin):
    list_display = ("brand", "category")
    search_fields = ("category", "brand__name")
    list_filter = ("brand",)


@admin.register(BrandFeature)
class BrandFeatureAdmin(admin.ModelAdmin):
    list_display = ("brand", "feature_name", "is_active")
    list_filter = ("brand", "is_active")
    search_fields = ("feature_name", "brand__name")


