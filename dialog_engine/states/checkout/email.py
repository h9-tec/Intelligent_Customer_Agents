from __future__ import annotations

from typing import Iterable

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class EmailState(BaseChatState):
    def handle(self) -> Iterable[object]:
        email = self.event.get("text", "").strip()
        try:
            validate_email(email)
        except ValidationError:
            yield TextMessage(to=self.chat.customer.phone, text="Please provide a valid email address.")
            return
        self.chat.customer.email = email
        self.chat.customer.save(update_fields=["email"])
        yield TextMessage(to=self.chat.customer.phone, text="Email updated.")


