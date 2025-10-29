from __future__ import annotations

from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("phone", "name", "email", "created_at")
    search_fields = ("phone", "name", "email")
    list_filter = ("created_at",)


