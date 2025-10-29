from __future__ import annotations

from typing import Any

from django.conf import settings

from project_core.llm import get_llm_client, get_model_id
from ai_assistant.prompts import CLASSIFIER_SYSTEM_PROMPT
from .taxonomies import CATEGORIES


client = get_llm_client()


def classify_intent(text: str, language: str = "en") -> str:
    model = get_model_id("classify")
    messages: list[dict[str, str]] = [
        {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
        {"role": "user", "content": f"Language: {language}. Text: {text}"},
    ]
    try:
        resp = client.chat.completions.create(model=model, messages=messages, temperature=0)
        content = resp.choices[0].message.content.strip()  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - allow offline/dev
        content = "Irrelevant"
    # Validate against categories
    if content not in CATEGORIES:
        return "Irrelevant"
    return content


