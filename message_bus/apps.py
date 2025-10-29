from __future__ import annotations

from django.apps import AppConfig


class MessageBusConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "message_bus"


