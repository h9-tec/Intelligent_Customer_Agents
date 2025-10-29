from __future__ import annotations

from django.db import models


class BrandProfile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    logo = models.ImageField(upload_to="brand/logo/", blank=True, null=True)
    theme_color = models.CharField(max_length=32, blank=True, default="#000000")
    language_default = models.CharField(max_length=8, default="en")

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class BrandTaxonomy(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE, related_name="taxonomies")
    category = models.CharField(max_length=255)
    subcategories = models.JSONField(default=list, blank=True)
    keywords = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ("brand", "category")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.brand.name} / {self.category}"


class BrandFeature(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE, related_name="features")
    feature_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("brand", "feature_name")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.brand.name}: {self.feature_name}"


