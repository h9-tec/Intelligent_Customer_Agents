from __future__ import annotations

from django.db import models


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    language = models.CharField(max_length=4, default="en")
    category = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.question[:60]


class FaqEmbedding(models.Model):
    faq = models.OneToOneField(Faq, on_delete=models.CASCADE, related_name="embedding")
    embedding = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)


