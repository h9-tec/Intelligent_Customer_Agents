from __future__ import annotations

from typing import Iterable

from django.conf import settings
from message_bus.message_types import TextMessage
from orders.utils import _get_active_cart, calculate_total
from ...states.abstract.chat_state import BaseChatState


class CheckoutState(BaseChatState):
    def handle(self) -> Iterable[object]:
        language = self.event.get("language", "en")
        customer = self.chat.customer
        
        # Check if cart is empty
        cart = _get_active_cart(customer)
        items = list(cart.items.select_related("product"))
        
        if not items:
            empty_cart_msg = {
                "en": "Your cart is empty. Please add items before checkout.",
                "ar": "سلة التسوق فارغة. يرجى إضافة منتجات قبل الشراء.",
            }
            yield TextMessage(
                to=customer.phone, 
                text=empty_cart_msg.get(language, empty_cart_msg["en"])
            )
            return
        
        # Validate stock availability
        out_of_stock_items = []
        for item in items:
            if item.product.stock < item.quantity:
                out_of_stock_items.append(item.product.sku)
        
        if out_of_stock_items:
            stock_error_msg = {
                "en": f"Some items are out of stock: {', '.join(out_of_stock_items)}. Please update your cart.",
                "ar": f"بعض المنتجات غير متوفرة: {', '.join(out_of_stock_items)}. يرجى تحديث السلة.",
            }
            yield TextMessage(
                to=customer.phone,
                text=stock_error_msg.get(language, stock_error_msg["en"])
            )
            return
        
        # Check if customer has address and email
        needs_address = not customer.address
        needs_email = not customer.email
        
        if needs_address:
            address_prompt_msg = {
                "en": "Please provide your shipping address.",
                "ar": "يرجى تقديم عنوان الشحن.",
            }
            yield TextMessage(
                to=customer.phone,
                text=address_prompt_msg.get(language, address_prompt_msg["en"])
            )
            # Set state to wait for address
            self.chat.current_state = "AddressState"
            self.chat.save(update_fields=["current_state"])
            return
        
        if needs_email:
            email_prompt_msg = {
                "en": "Please provide your email address for order confirmation.",
                "ar": "يرجى تقديم عنوان البريد الإلكتروني لتأكيد الطلب.",
            }
            yield TextMessage(
                to=customer.phone,
                text=email_prompt_msg.get(language, email_prompt_msg["en"])
            )
            # Set state to wait for email
            self.chat.current_state = "EmailState"
            self.chat.save(update_fields=["current_state"])
            return
        
        # Customer has address and email, proceed to shipping selection
        total = calculate_total(items)
        currency = getattr(settings, "DEFAULT_CURRENCY", "USD")
        
        cart_summary_msg = {
            "en": f"Cart total: {total.grand_total} {currency}. Choose shipping method:",
            "ar": f"الإجمالي: {total.grand_total} {currency}. اختر طريقة الشحن:",
        }
        
        # Route to shipping selection
        from .choose_shipping import ChooseShippingState
        shipping_state = ChooseShippingState(self.chat, self.event)
        yield from shipping_state.handle()


