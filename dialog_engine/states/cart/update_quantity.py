from __future__ import annotations

from typing import Iterable

from inventory.models import Product
from message_bus.message_types import TextMessage
from orders.utils import update_quantity
from ...states.abstract.chat_state import BaseChatState
from ...state_utils import parse_button_id


class UpdateQuantityState(BaseChatState):
    def handle(self) -> Iterable[object]:
        # Expect button_id: UpdateQuantityState_<product_id>_<qty>
        button_id = self.event.get("button_id", "")
        _, args = parse_button_id(button_id)
        if len(args) < 2:
            yield TextMessage(to=self.chat.customer.phone, text="Missing parameters.")
            return
        product_id = int(args[0])
        qty = int(args[1])
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            yield TextMessage(to=self.chat.customer.phone, text="Product not found.")
            return
        try:
            update_quantity(self.chat.customer, product, quantity=qty)
        except Exception as e:
            yield TextMessage(to=self.chat.customer.phone, text=str(e))
            return
        yield TextMessage(to=self.chat.customer.phone, text=f"Updated quantity to {qty}.")


