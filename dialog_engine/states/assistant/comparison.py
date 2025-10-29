from __future__ import annotations

from typing import Iterable

from ai_assistant.assistant import compare_products
from message_bus.message_types import TextMessage
from ...states.abstract.chat_state import BaseChatState


class ComparisonState(BaseChatState):
    def handle(self) -> Iterable[object]:
        text = self.event.get("text", "")
        language = self.event.get("language", "en")
        # Expect ids in event args or simple parsing "compare: 1,2"
        ids_str = self.event.get("ids") or ""
        product_ids: list[int] = []
        if ids_str:
            product_ids = [int(x) for x in ids_str.split("-") if x.isdigit()]
        if not product_ids:
            # Try parse from text like "1,2"
            tokens = [t.strip().strip(",") for t in text.replace("compare", "").split()]
            product_ids = [int(t) for t in tokens if t.isdigit()]
        if not product_ids:
            yield TextMessage(to=self.chat.customer.phone, text="Please provide product IDs to compare.")
            return
        result = compare_products(product_ids, self.chat, language)
        yield TextMessage(to=self.chat.customer.phone, text=result or "Comparison is not available right now.")


