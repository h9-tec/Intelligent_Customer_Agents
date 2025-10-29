from __future__ import annotations

import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_hook_verify_token(client, settings):
    settings.WA_VERIFY_TOKEN = "abc"
    url = "/hook/verify/"
    resp = client.get(url, {"hub.verify_token": "abc", "hub.challenge": "123"})
    assert resp.status_code == 200
    assert resp.content == b"123"


@pytest.mark.django_db
def test_hook_post_enqueues_task(client, monkeypatch):
    called = {"ok": False}

    def fake_delay(data):
        called["ok"] = True

    monkeypatch.setattr("wa_gateway.tasks.process_inbound_message.delay", fake_delay)
    url = "/hook/"
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {"from": "+1", "timestamp": "0", "type": "text", "text": {"body": "hi"}}
                            ]
                        }
                    }
                ]
            }
        ]
    }
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    assert called["ok"] is True


