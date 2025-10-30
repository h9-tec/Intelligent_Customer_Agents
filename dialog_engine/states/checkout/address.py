from __future__ import annotations

from typing import Iterable

from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class AddressState(BaseChatState):
    def handle(self) -> Iterable[object]:
        language = self.event.get("language", "en")
        address = self.event.get("text", "").strip()
        
        if not address:
            address_prompt_msg = {
                "en": "Please provide your shipping address.",
                "ar": "يرجى تقديم عنوان الشحن.",
            }
            yield TextMessage(
                to=self.chat.customer.phone,
                text=address_prompt_msg.get(language, address_prompt_msg["en"])
            )
            return
        
        # Save address
        self.chat.customer.address = address
        self.chat.customer.save(update_fields=["address"])
        
        address_saved_msg = {
            "en": "Address updated. Continuing checkout...",
            "ar": "تم تحديث العنوان. متابعة الشراء...",
        }
        yield TextMessage(
            to=self.chat.customer.phone,
            text=address_saved_msg.get(language, address_saved_msg["en"])
        )
        
        # Check if email is needed, otherwise proceed to shipping
        if not self.chat.customer.email:
            from .email import EmailState
            email_state = EmailState(self.chat, self.event)
            yield from email_state.handle()
        else:
            # Continue checkout flow - proceed to shipping selection
            from .choose_shipping import ChooseShippingState
            shipping_state = ChooseShippingState(self.chat, self.event)
            yield from shipping_state.handle()


