from __future__ import annotations

from typing import Iterable

from ai_assistant.services.recommend_products import recommend_products_for_query
from message_bus.message_types import Button, ButtonsMessage, TextMessage
from ...states.abstract.chat_state import BaseChatState


class ShowProductsState(BaseChatState):
    def handle(self) -> Iterable[object]:
        query = self.event.get("text", "")
        language = self.event.get("language", "en")
        products = recommend_products_for_query(query, language=language)[:5]
        if not products:
            yield TextMessage(to=self.chat.customer.phone, text="I couldn't find matching products.")
            return
        lines = []
        buttons = []
        for p in products:
            name = next((n.name for n in p.names.all() if n.language == language), None) or p.sku
            lines.append(f"- {name} | ${p.base_price}")
            buttons.append(Button(id=f"AddQuantityState_{p.id}_1", title=f"Add {name}"))
        yield TextMessage(to=self.chat.customer.phone, text="Here are some options:\n" + "\n".join(lines))
        yield ButtonsMessage(to=self.chat.customer.phone, body="Add to cart:", buttons=buttons[:3])


