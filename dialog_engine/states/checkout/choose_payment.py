from __future__ import annotations

from typing import Iterable

from message_bus.message_types import Button, ButtonsMessage, TextMessage
from ...states.abstract.chat_state import BaseChatState


class ChoosePaymentState(BaseChatState):
    def handle(self) -> Iterable[object]:
        # Expect button id: ChoosePaymentState_<shipping_id>_<payment_id>
        button_id = self.event.get("button_id", "")
        parts = button_id.split("_")
        if len(parts) >= 3:
            shipping_id = parts[1]
            payment_id = parts[2]
            yield ButtonsMessage(
                to=self.chat.customer.phone,
                body="Confirm order?",
                buttons=[Button(id=f"OrderFinishedState_{shipping_id}_{payment_id}", title="Place Order")],
            )
            return
        yield TextMessage(to=self.chat.customer.phone, text="Please choose a payment method.")


