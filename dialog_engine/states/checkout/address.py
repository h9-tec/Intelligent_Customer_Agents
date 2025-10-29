from __future__ import annotations

from typing import Iterable

from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class AddressState(BaseChatState):
    def handle(self) -> Iterable[object]:
        address = self.event.get("text", "").strip()
        if not address:
            yield TextMessage(to=self.chat.customer.phone, text="Please provide a shipping address.")
            return
        self.chat.customer.address = address
        self.chat.customer.save(update_fields=["address"])
        yield TextMessage(to=self.chat.customer.phone, text="Address updated.")


