from __future__ import annotations

from django.apps import AppConfig


class DialogEngineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dialog_engine"

    def ready(self) -> None:  # pragma: no cover
        from .signals import message_received
        from .engine import ChatEngine

        def _on_message(sender, **kwargs):
            event = kwargs.get("event")
            if event:
                ChatEngine().handle_message(event)

        message_received.connect(_on_message, dispatch_uid="dialog_engine_on_message")


