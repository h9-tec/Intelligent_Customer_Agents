from __future__ import annotations

from typing import Iterable

from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class ResetConversationState(BaseChatState):
    def handle(self) -> Iterable[object]:
        self.chat.current_state = None
        self.chat.save(update_fields=["current_state"])
        yield TextMessage(to=self.chat.customer.phone, text="Conversation has been reset.")


