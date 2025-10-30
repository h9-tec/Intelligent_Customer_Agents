from __future__ import annotations

from typing import Iterable

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class EmailState(BaseChatState):
    def handle(self) -> Iterable[object]:
        language = self.event.get("language", "en")
        email = self.event.get("text", "").strip()
        
        try:
            validate_email(email)
        except ValidationError:
            email_error_msg = {
                "en": "Please provide a valid email address.",
                "ar": "يرجى تقديم عنوان بريد إلكتروني صالح.",
            }
            yield TextMessage(
                to=self.chat.customer.phone,
                text=email_error_msg.get(language, email_error_msg["en"])
            )
            return
        
        # Save email
        self.chat.customer.email = email
        self.chat.customer.save(update_fields=["email"])
        
        email_saved_msg = {
            "en": "Email updated. Continuing checkout...",
            "ar": "تم تحديث البريد الإلكتروني. متابعة الشراء...",
        }
        yield TextMessage(
            to=self.chat.customer.phone,
            text=email_saved_msg.get(language, email_saved_msg["en"])
        )
        
        # Continue checkout flow - proceed to shipping selection
        from .choose_shipping import ChooseShippingState
        shipping_state = ChooseShippingState(self.chat, self.event)
        yield from shipping_state.handle()


