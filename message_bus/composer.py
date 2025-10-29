from __future__ import annotations

from typing import Iterable

from conversation_log.models import Chat, Message
from wa_client.api import WhatsAppClient
from .message_types import (
    Button,
    ButtonsMessage,
    CartMessage,
    ImageMessage,
    ListMessage,
    ProductListMessage,
    ProductMessage,
    TextMessage,
)


def _estimate_tokens(text: str) -> int:
    # Rough token estimate: 1 token ~ 4 chars
    return max(1, len(text) // 4)


def compose_and_send(chat: Chat, messages_list: Iterable[object]) -> None:
    client = WhatsAppClient()
    to = chat.customer.phone
    for msg in messages_list:
        if isinstance(msg, TextMessage):
            client.send_text(to, msg.text)
            Message.objects.create(chat=chat, content=msg.text, response="", tokens=_estimate_tokens(msg.text))
        elif isinstance(msg, ButtonsMessage):
            client.send_buttons(
                to,
                body=msg.body,
                buttons=[{"id": b.id, "title": b.title} for b in msg.buttons],
            )
            Message.objects.create(chat=chat, content=msg.body, response="", tokens=_estimate_tokens(msg.body))
        elif isinstance(msg, ListMessage):
            client.send_list(to, header=msg.header, title=msg.title, sections=list(msg.sections))
            Message.objects.create(chat=chat, content=msg.title, response="", tokens=_estimate_tokens(msg.title))
        elif isinstance(msg, ImageMessage):
            client.send_image(to, image_url=msg.image_url, caption=msg.caption)
            caption = msg.caption or ""
            Message.objects.create(chat=chat, content=caption, response="", tokens=_estimate_tokens(caption))
        elif isinstance(msg, ProductMessage):
            client.send_product(to, product_id=str(msg.product_id), title=msg.title, price=msg.price, image_url=msg.image_url)
            content = f"{msg.title} {msg.price}"
            Message.objects.create(chat=chat, content=content, response="", tokens=_estimate_tokens(content))
        elif isinstance(msg, ProductListMessage):
            client.send_product_list(to, products=list(msg.products), header=msg.header or "", body=msg.body or "")
            content = msg.body or "Products"
            Message.objects.create(chat=chat, content=content, response="", tokens=_estimate_tokens(content))
        elif isinstance(msg, CartMessage):
            body = "\n".join([f"{it['name']} x{it['qty']} = {it['subtotal']}" for it in msg.items])
            client.send_text(to, f"Cart\n{body}\nTotal: {msg.total}")
            Message.objects.create(chat=chat, content=body, response="", tokens=_estimate_tokens(body))


