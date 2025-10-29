from __future__ import annotations

from typing import Iterable

from django.utils import timezone

from message_bus.message_types import TextMessage
from orders.models import ShippingOption
from orders.utils import create_order, finalize_order, get_last_order
from payments.models import PaymentOptions
from ...states.abstract.chat_state import BaseChatState


class OrderFinishedState(BaseChatState):
    def handle(self) -> Iterable[object]:
        # Expect button id: OrderFinishedState_<shipping_id>_<payment_id>
        button_id = self.event.get("button_id", "")
        parts = button_id.split("_")
        if len(parts) < 3:
            yield TextMessage(to=self.chat.customer.phone, text="Order confirmation failed.")
            return
        shipping_id = int(parts[1])
        payment_id = int(parts[2])
        shipping = ShippingOption.objects.filter(pk=shipping_id).first()
        payment = PaymentOptions.objects.filter(pk=payment_id).first()
        try:
            order = create_order(self.chat.customer, shipping=shipping, payment_option=payment)
            order = finalize_order(order)
            msg = f"Order {order.order_number} placed. Total: {order.total_price}"
        except Exception as e:
            msg = f"Order failed: {e}"
        yield TextMessage(to=self.chat.customer.phone, text=msg)


