from __future__ import annotations

from typing import Type

from .states.abstract.chat_state import BaseChatState
from .states.assistant.assistant import AssistantState
from .states.assistant.show_cart import ShowCartState
from .states.assistant.comparison import ComparisonState
from .states.assistant.reset import ResetConversationState
from .states.assistant.show_products import ShowProductsState
from .states.assistant.faq import FaqState
from .states.assistant.invalid_classification import InvalidClassificationState
from .states.assistant.irrelevant import IrrelevantQuestionState
from .states.cart.add_quantity import AddQuantityState
from .states.cart.update_quantity import UpdateQuantityState
from .states.cart.remove_quantity import RemoveQuantityState
from .states.cart.product_added import ProductAddedState
from .states.cart.product_updated import ProductUpdatedState
from .states.cart.product_removed import ProductRemovedState
from .states.checkout.checkout import CheckoutState
from .states.checkout.address import AddressState
from .states.checkout.email import EmailState
from .states.checkout.choose_shipping import ChooseShippingState
from .states.checkout.choose_payment import ChoosePaymentState
from .states.checkout.order_finished import OrderFinishedState
from .states.checkout.cancel_order import CancelOrderState


STATE_REGISTRY: dict[str, Type[BaseChatState]] = {
    "AssistantState": AssistantState,
    "ShowCartState": ShowCartState,
    "ComparisonState": ComparisonState,
    "ResetConversationState": ResetConversationState,
    "ShowProductsState": ShowProductsState,
    "FaqState": FaqState,
    "InvalidClassificationState": InvalidClassificationState,
    "IrrelevantQuestionState": IrrelevantQuestionState,
    # Cart
    "AddQuantityState": AddQuantityState,
    "UpdateQuantityState": UpdateQuantityState,
    "RemoveQuantityState": RemoveQuantityState,
    "ProductAddedState": ProductAddedState,
    "ProductUpdatedState": ProductUpdatedState,
    "ProductRemovedState": ProductRemovedState,
    # Checkout
    "CheckoutState": CheckoutState,
    "AddressState": AddressState,
    "EmailState": EmailState,
    "ChooseShippingState": ChooseShippingState,
    "ChoosePaymentState": ChoosePaymentState,
    "OrderFinishedState": OrderFinishedState,
    "CancelOrderState": CancelOrderState,
}

BUTTON_REGISTRY: dict[str, Type[BaseChatState]] = {
    # Assistant shortcuts
    "ShowCartState": ShowCartState,
    "CheckoutState": CheckoutState,
    "ShowProductsState": ShowProductsState,
    "ComparisonState": ComparisonState,
    "FaqState": FaqState,
    "ResetConversationState": ResetConversationState,
    # Cart
    "AddQuantityState": AddQuantityState,
    "UpdateQuantityState": UpdateQuantityState,
    "RemoveQuantityState": RemoveQuantityState,
    # Checkout
    "ChooseShippingState": ChooseShippingState,
    "ChoosePaymentState": ChoosePaymentState,
    "OrderFinishedState": OrderFinishedState,
    "CancelOrderState": CancelOrderState,
}

ACTION_BUTTONS = {
    "cart": "ShowCartState",
    "checkout": "CheckoutState",
    "reset": "ResetConversationState",
}


