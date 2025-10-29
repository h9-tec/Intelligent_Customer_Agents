from __future__ import annotations

from django.db import models

from inventory.models import Product


class ProductEmbedding(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="embedding")
    language = models.CharField(max_length=4, default="en")
    product_text = models.TextField()
    embedding = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)


class Recommendation(models.Model):
    customer_input = models.TextField()
    embedding = models.BinaryField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RecommendationProduct(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name="items")
    product_embedding = models.ForeignKey(ProductEmbedding, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)

    class Meta:
        unique_together = ("recommendation", "product_embedding")


