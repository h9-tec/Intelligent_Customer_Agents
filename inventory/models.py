from __future__ import annotations

from django.db import models

from brandkit.models import BrandProfile


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children"
    )
    brand = models.ForeignKey(BrandProfile, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ("name", "parent", "brand")

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.PROTECT, related_name="products")
    sku = models.CharField(max_length=64, unique=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="products/images/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    specifications = models.JSONField(default=dict, blank=True)
    compatibility = models.JSONField(default=dict, blank=True)
    warranty_months = models.IntegerField(default=12)
    created_at = models.DateTimeField(auto_now_add=True)

    # Electronics-specific
    manufacturer = models.CharField(max_length=255, blank=True, default="")
    model_number = models.CharField(max_length=255, blank=True, default="")
    release_year = models.IntegerField(blank=True, null=True)
    technical_specs = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["sku"], name="idx_product_sku"),
            models.Index(fields=["is_active"], name="idx_product_active"),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.sku}"


class ProductName(models.Model):
    LANG_CHOICES = (
        ("en", "English"),
        ("ar", "Arabic"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="names")
    name = models.CharField(max_length=512)
    language = models.CharField(max_length=4, choices=LANG_CHOICES, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "language")


class ProductDescription(models.Model):
    LANG_CHOICES = (
        ("en", "English"),
        ("ar", "Arabic"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="descriptions")
    description = models.TextField()
    language = models.CharField(max_length=4, choices=LANG_CHOICES, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "language")


