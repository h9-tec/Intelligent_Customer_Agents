from __future__ import annotations

from django.contrib import admin

from .models import Faq, FaqEmbedding


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("question", "language", "category", "is_active", "created_at")
    list_filter = ("language", "is_active", "category")
    search_fields = ("question", "answer")


@admin.register(FaqEmbedding)
class FaqEmbeddingAdmin(admin.ModelAdmin):
    list_display = ("faq", "created_at")
    search_fields = ("faq__question",)


