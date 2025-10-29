from __future__ import annotations

from typing import Iterable

from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class CheckoutState(BaseChatState):
    def handle(self) -> Iterable[object]:
        yield TextMessage(to=self.chat.customer.phone, text="Proceeding to checkout (stub)")


