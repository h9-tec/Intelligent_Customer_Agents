from __future__ import annotations

from celery import shared_task
from django.conf import settings

from .utils import cleanup_abandoned_chats as _cleanup


@shared_task
def cleanup_abandoned_chats() -> int:
    days = getattr(settings, "ABANDONED_CHAT_DAYS", 30)
    return _cleanup(days)


