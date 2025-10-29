from __future__ import annotations

from celery import shared_task
from django.conf import settings

from .utils import check_abandoned_carts


@shared_task
def cleanup_abandoned_carts() -> int:
    days = getattr(settings, "ABANDONED_CART_DAYS", 7)
    return check_abandoned_carts(days)


