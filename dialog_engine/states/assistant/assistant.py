from __future__ import annotations

from typing import Iterable

from conversation_log.models import Chat
from intent_classifier.api import classify_intent
from message_bus.message_types import Button, ButtonsMessage, TextMessage
from .show_cart import ShowCartState
from .show_products import ShowProductsState
from .faq import FaqState
from .comparison import ComparisonState
from .reset import ResetConversationState
from .invalid_classification import InvalidClassificationState
from .irrelevant import IrrelevantQuestionState
from ...states.abstract.chat_state import BaseChatState


class AssistantState(BaseChatState):
    def handle(self) -> Iterable[object]:
        text = self.event.get("text", "").strip()
        language = self.event.get("language", "en")
        intent = classify_intent(text, language)
        if intent == "Cart":
            return list(ShowCartState(self.chat, self.event).handle())
        if intent == "Recommendation":
            return list(ShowProductsState(self.chat, self.event).handle())
        if intent == "FAQ":
            return list(FaqState(self.chat, self.event).handle())
        if intent == "Comparison":
            return list(ComparisonState(self.chat, self.event).handle())
        if intent == "Reset Conversation":
            return list(ResetConversationState(self.chat, self.event).handle())
        if intent == "Irrelevant":
            return list(IrrelevantQuestionState(self.chat, self.event).handle())
        greeting = {
            "en": "How can I help you with electronics today?",
            "ar": "كيف أستطيع مساعدتك في الإلكترونيات اليوم؟",
        }
        yield TextMessage(to=self.chat.customer.phone, text=greeting.get(language, greeting["en"]))
        yield ButtonsMessage(
            to=self.chat.customer.phone,
            body="Choose an action",
            buttons=[Button(id="ShowCartState", title="Cart"), Button(id="CheckoutState", title="Checkout")],
        )


