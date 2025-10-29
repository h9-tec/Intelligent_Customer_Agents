from __future__ import annotations

from typing import Iterable

from helpdesk.utils import recommend_faqs
from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class FaqState(BaseChatState):
    def handle(self) -> Iterable[object]:
        query = self.event.get("text", "")
        language = self.event.get("language", "en")
        faqs = recommend_faqs(query, language=language, top_k=3)
        if not faqs:
            yield TextMessage(to=self.chat.customer.phone, text="No related FAQs found.")
            return
        lines = [f"Q: {f.question}\nA: {f.answer}" for f in faqs]
        yield TextMessage(to=self.chat.customer.phone, text="\n\n".join(lines))


