from __future__ import annotations

from typing import Iterable

from message_bus.message_types import Button, ButtonsMessage, TextMessage
from orders.models import ShippingOption
from ...states.abstract.chat_state import BaseChatState


class ChooseShippingState(BaseChatState):
    def handle(self) -> Iterable[object]:
        # If invoked by button with shipping id, proceed to payment selection
        button_id = self.event.get("button_id")
        if button_id and "_" in button_id:
            # button id might be ChooseShippingState_<shipping_id>
            try:
                shipping_id = int(button_id.split("_")[1])
            except Exception:
                shipping_id = None
            if shipping_id:
                # Build payment selection buttons
                from payments.models import PaymentOptions

                buttons = []
                for po in PaymentOptions.objects.filter(is_active=True):
                    buttons.append(Button(id=f"ChoosePaymentState_{shipping_id}_{po.id}", title=po.name))
                yield ButtonsMessage(to=self.chat.customer.phone, body="Choose payment method:", buttons=buttons[:3])
                return

        # Otherwise present shipping options
        options = ShippingOption.objects.filter(is_active=True).order_by("price")
        if not options:
            yield TextMessage(to=self.chat.customer.phone, text="No shipping options available.")
            return
        buttons = [Button(id=f"ChooseShippingState_{opt.id}", title=f"{opt.name} ${opt.price}") for opt in options]
        yield ButtonsMessage(to=self.chat.customer.phone, body="Choose shipping:", buttons=buttons[:3])


