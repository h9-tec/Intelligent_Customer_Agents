from __future__ import annotations

from typing import Iterable

from django.db import transaction
from django.utils import timezone

from message_bus.message_types import TextMessage
from orders.models import ShippingOption
from orders.utils import create_order, finalize_order, get_last_order
from payments.models import Payment, PaymentOptions
from ...states.abstract.chat_state import BaseChatState


class OrderFinishedState(BaseChatState):
    def handle(self) -> Iterable[object]:
        # Expect button id: OrderFinishedState_<shipping_id>_<payment_id>
        button_id = self.event.get("button_id", "")
        parts = button_id.split("_")
        if len(parts) < 3:
            yield TextMessage(to=self.chat.customer.phone, text="Order confirmation failed.")
            return
        
        try:
            shipping_id = int(parts[1])
            payment_id = int(parts[2])
        except ValueError:
            yield TextMessage(to=self.chat.customer.phone, text="Invalid order confirmation. Please try again.")
            return
        
        shipping = ShippingOption.objects.filter(pk=shipping_id).first()
        payment_option = PaymentOptions.objects.filter(pk=payment_id).first()
        
        if not shipping or not payment_option:
            yield TextMessage(
                to=self.chat.customer.phone,
                text="Shipping or payment option not found. Please start checkout again."
            )
            return
        
        try:
            with transaction.atomic():
                # Create order
                order = create_order(
                    self.chat.customer,
                    shipping=shipping,
                    payment_option=payment_option
                )
                
                # Create payment record
                payment = Payment.objects.create(
                    customer=self.chat.customer,
                    order=order,
                    amount=order.total_price,
                    payment_option=payment_option,
                    status=Payment.Status.PENDING
                )
                
                # Capture payment (simulates payment gateway capture)
                # In production, this would call the actual payment gateway API
                transaction_id = f"TXN-{order.order_number}-{payment.id}"
                payment.capture(transaction_id=transaction_id)
                
                # Finalize order (decrement stock)
                order = finalize_order(order)
                
                msg = (
                    f"✅ Order {order.order_number} placed successfully!\n"
                    f"Total: ${order.total_price}\n"
                    f"Payment: {payment_option.name}\n"
                    f"Transaction ID: {transaction_id}"
                )
                
        except ValueError as e:
            msg = f"Order failed: {str(e)}. Please check your cart and try again."
        except Exception as e:
            msg = f"Order processing error: {str(e)}. Please contact support."
        
        yield TextMessage(to=self.chat.customer.phone, text=msg)


