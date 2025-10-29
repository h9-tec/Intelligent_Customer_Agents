from __future__ import annotations

import threading
from typing import Any, Iterable

import requests
from django.conf import settings

from .endpoints import messages_url


class _Singleton(type):
    _instances: dict[type, "WhatsAppClient"] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):  # type: ignore[override]
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class WhatsAppClient(metaclass=_Singleton):
    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {settings.WA_BEARER_TOKEN}",
                "Content-Type": "application/json",
            }
        )
        self._phone_id = settings.WA_PHONE_ID

    def _post(self, payload: dict[str, Any]) -> requests.Response:
        url = messages_url(self._phone_id)
        resp = self._session.post(url, json=payload, timeout=20)
        resp.raise_for_status()
        return resp

    def send_text(self, to: str, text: str) -> None:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text},
        }
        self._post(payload)

    def send_buttons(self, to: str, body: str, buttons: list[dict[str, str]]) -> None:
        # buttons: [{id, title}]
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": b["id"], "title": b["title"]}} for b in buttons
                    ]
                },
            },
        }
        self._post(payload)

    def send_list(self, to: str, header: str, title: str, sections: list[dict[str, Any]]) -> None:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": header},
                "body": {"text": title},
                "action": {"sections": sections},
            },
        }
        self._post(payload)

    def send_image(self, to: str, image_url: str, caption: str | None = None) -> None:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {"link": image_url, **({"caption": caption} if caption else {})},
        }
        self._post(payload)

    def send_product(self, to: str, product_id: str, title: str, price: str, image_url: str | None = None) -> None:
        # Fallback: send as text with optional image
        if image_url:
            self.send_image(to, image_url=image_url, caption=f"{title} — {price}")
        else:
            self.send_text(to, f"{title} — {price}")

    def send_product_list(self, to: str, products: list[dict[str, Any]], header: str, body: str) -> None:
        # Fallback: render as text list with buttons limited to 3 items
        lines = []
        buttons: list[dict[str, str]] = []
        for p in products[:3]:
            lines.append(f"- {p.get('title')} — {p.get('price')}")
            pid = str(p.get("id")) if p.get("id") is not None else ""
            buttons.append({"id": f"AddQuantityState_{pid}_1", "title": f"Add {p.get('title')}"})
        text_body = (header + "\n" if header else "") + (body or "Products") + "\n" + "\n".join(lines)
        self.send_text(to, text_body)
        if buttons:
            self.send_buttons(to, body="Quick add:", buttons=buttons)

    def mark_read(self, message_id: str) -> None:
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        self._post(payload)


get_client = WhatsAppClient


