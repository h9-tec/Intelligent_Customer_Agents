from __future__ import annotations

from typing import Iterable

from inventory.models import Product
from message_bus.message_types import TextMessage
from orders.utils import remove_from_cart
from ...states.abstract.chat_state import BaseChatState
from ...state_utils import parse_button_id


class RemoveQuantityState(BaseChatState):
    def handle(self) -> Iterable[object]:
        # Expect button_id: RemoveQuantityState_<product_id>
        button_id = self.event.get("button_id", "")
        _, args = parse_button_id(button_id)
        if len(args) < 1:
            yield TextMessage(to=self.chat.customer.phone, text="Missing product id.")
            return
        product_id = int(args[0])
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            yield TextMessage(to=self.chat.customer.phone, text="Product not found.")
            return
        remove_from_cart(self.chat.customer, product)
        yield TextMessage(to=self.chat.customer.phone, text="Item removed from cart.")


