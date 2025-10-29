from __future__ import annotations

from typing import Iterable

from inventory.models import Product
from message_bus.message_types import Button, ButtonsMessage, TextMessage
from orders.utils import add_to_cart
from ...states.abstract.chat_state import BaseChatState
from ...state_utils import parse_button_id


class AddQuantityState(BaseChatState):
    def handle(self) -> Iterable[object]:
        # Expect button_id: AddQuantityState_<product_id>_<qty>
        button_id = self.event.get("button_id", "")
        _, args = parse_button_id(button_id)
        if len(args) < 1:
            yield TextMessage(to=self.chat.customer.phone, text="Missing product id.")
            return
        product_id = int(args[0])
        qty = int(args[1]) if len(args) > 1 else 1
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            yield TextMessage(to=self.chat.customer.phone, text="Product not found.")
            return
        try:
            add_to_cart(self.chat.customer, product, quantity=qty)
        except Exception as e:
            yield TextMessage(to=self.chat.customer.phone, text=str(e))
            return
        yield TextMessage(to=self.chat.customer.phone, text=f"Added {qty} to cart.")
        yield ButtonsMessage(
            to=self.chat.customer.phone,
            body="Next",
            buttons=[
                Button(id="ShowCartState", title="View Cart"),
                Button(id="CheckoutState", title="Checkout"),
            ],
        )


