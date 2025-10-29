from __future__ import annotations

import pytest

from dialog_engine.engine import ChatEngine


@pytest.mark.django_db
def test_engine_handles_text(monkeypatch, customer):
    # Avoid sending real messages
    sent = {"count": 0}

    def fake_compose(chat, msgs):
        sent["count"] += len(list(msgs))

    monkeypatch.setattr("message_bus.composer.compose_and_send", fake_compose)

    event = {"sender": customer.phone, "event_type": "text", "text": "hello"}
    ChatEngine().handle_message(event)
    assert sent["count"] >= 1


