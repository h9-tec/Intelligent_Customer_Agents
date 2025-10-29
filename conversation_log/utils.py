from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from users.models import Customer
from .models import Chat, Message


def get_or_create_chat(customer: Customer) -> Chat:
    chat, _ = Chat.objects.get_or_create(customer=customer, is_active=True)
    return chat


def create_message(
    chat: Chat, content: str, response: str = "", state: str = "", language: str = "en", tokens: int = 0
) -> Message:
    msg = Message.objects.create(
        chat=chat, content=content, response=response, state=state, language=language, tokens=tokens
    )
    chat.touch()
    return msg


def cleanup_abandoned_chats(days: int) -> int:
    threshold = timezone.now() - timedelta(days=days)
    qs = Chat.objects.filter(is_active=True, last_message_date__lt=threshold)
    count = qs.count()
    qs.update(is_active=False)
    return count


