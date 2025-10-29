from __future__ import annotations

from typing import Iterable

from django.conf import settings

from project_core.llm import get_llm_client, get_model_id
from .prompts import ASSISTANT_SYSTEM_PROMPT
from conversation_log.models import Chat, Message
from inventory.models import Product, ProductDescription, ProductName


client = get_llm_client()


def get_context(chat: Chat, max_tokens: int | None = None) -> list[Message]:
    max_tokens = max_tokens or getattr(settings, "TOKENS_MAX", 3000)
    messages = list(chat.messages.order_by("-created_at")[:50])
    total = 0
    selected: list[Message] = []
    for msg in messages:
        total += max(1, msg.tokens)
        if total > max_tokens:
            break
        selected.append(msg)
    return list(reversed(selected))


def _format_product_context(product_ids: Iterable[int], language: str) -> str:
    parts: list[str] = []
    for pid in product_ids:
        try:
            p = Product.objects.get(pk=pid)
        except Product.DoesNotExist:  # pragma: no cover
            continue
        name = ProductName.objects.filter(product=p, language=language).first() or ProductName.objects.filter(
            product=p, language="en"
        ).first()
        desc = ProductDescription.objects.filter(product=p, language=language).first()
        parts.append(
            f"Product: {name.name if name else p.sku}\nPrice: {p.base_price}\nSpecs: {p.specifications}\nDesc: {desc.description if desc else ''}"
        )
    return "\n\n".join(parts)


def get_related_info(query: str, chat: Chat, language: str = "en") -> str:
    model = get_model_id("chat")
    context_msgs = get_context(chat, getattr(settings, "TOKENS_MAX", 3000))
    context_text = "\n".join([m.content for m in context_msgs])
    system_prompt = ASSISTANT_SYSTEM_PROMPT
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Language: {language}. Context: {context_text}\nQuestion: {query}"},
            ],
            temperature=0.2,
        )
        return (resp.choices[0].message.content or "").strip()  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover
        return ""


def compare_products(product_ids: list[int], chat: Chat, language: str = "en") -> str:
    model = get_model_id("chat")
    product_context = _format_product_context(product_ids, language)
    system_prompt = ASSISTANT_SYSTEM_PROMPT + "\nFocus: Compare the following products in a concise table with key specs, pros/cons, and who it suits."
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": product_context},
            ],
            temperature=0.2,
        )
        return (resp.choices[0].message.content or "").strip()  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover
        return ""


