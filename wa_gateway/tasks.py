from __future__ import annotations

from celery import shared_task
from django.dispatch import Signal

# Import signal from dialog engine, but fallback to local signal if not ready yet
try:  # pragma: no cover
    from dialog_engine.signals import message_received
except Exception:  # pragma: no cover
    message_received = Signal()  # type: ignore[assignment]


@shared_task
def process_inbound_message(event_data: dict) -> None:
    message_received.send(sender="wa_gateway", event=event_data)


