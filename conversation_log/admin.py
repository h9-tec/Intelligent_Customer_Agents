from __future__ import annotations

from django.contrib import admin

from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("customer", "current_state", "language", "is_active", "last_message_date")
    list_filter = ("is_active", "language")
    search_fields = ("customer__phone", "customer__name")
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "state", "language", "tokens", "created_at")
    list_filter = ("language", "state")
    search_fields = ("content", "response")


