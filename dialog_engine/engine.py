from __future__ import annotations

from langdetect import detect

from conversation_log.utils import get_or_create_chat
from message_bus.composer import compose_and_send
from .state_router import BUTTON_REGISTRY, STATE_REGISTRY
from .state_utils import parse_button_id


class ChatEngine:
    def handle_message(self, event: dict) -> None:
        sender = event.get("sender")
        if not sender:
            return
        # Resolve chat
        from users.models import Customer

        customer, _ = Customer.objects.get_or_create(phone=sender)
        chat = get_or_create_chat(customer)

        # Determine language for text events
        if event.get("event_type") == "text":
            text = event.get("text", "")
            try:
                lang = detect(text)
            except Exception:  # pragma: no cover
                lang = "en"
            event["language"] = "ar" if lang.startswith("ar") else "en"

        # Route
        messages = []
        if event.get("event_type") == "button":
            button_id = event.get("button_id", "")
            prefix, _ = parse_button_id(button_id)
            state_cls = BUTTON_REGISTRY.get(prefix, STATE_REGISTRY.get("AssistantState"))
            state = state_cls(chat, event)
            messages = list(state.handle())
        else:
            state_cls = STATE_REGISTRY.get("AssistantState")
            state = state_cls(chat, event)
            messages = list(state.handle())

        compose_and_send(chat, messages)


