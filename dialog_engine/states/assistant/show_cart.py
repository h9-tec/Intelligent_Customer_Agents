from __future__ import annotations

from typing import Iterable

from message_bus.message_types import TextMessage
from orders.utils import _get_active_cart, calculate_total
from ...states.abstract.chat_state import BaseChatState


class ShowCartState(BaseChatState):
    def handle(self) -> Iterable[object]:
        cart = _get_active_cart(self.chat.customer)
        items = list(cart.items.select_related("product"))
        total = calculate_total(items)
        text = f"Cart items: {len(items)}\nTotal: {total.grand_total}"
        yield TextMessage(to=self.chat.customer.phone, text=text)


