from __future__ import annotations

from typing import Iterable

from message_bus.message_types import TextMessage
from orders.utils import cancel_order, get_last_order
from ...states.abstract.chat_state import BaseChatState


class CancelOrderState(BaseChatState):
    def handle(self) -> Iterable[object]:
        order = get_last_order(self.chat.customer)
        if not order:
            yield TextMessage(to=self.chat.customer.phone, text="No recent order found.")
            return
        cancel_order(order)
        yield TextMessage(to=self.chat.customer.phone, text=f"Order {order.order_number} cancelled.")


