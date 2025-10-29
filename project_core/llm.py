from __future__ import annotations

from typing import Tuple

from django.conf import settings
from openai import OpenAI


def get_llm_client() -> OpenAI:
    provider = getattr(settings, "LLM_PROVIDER", "openai").lower()
    if provider == "openrouter":
        return OpenAI(api_key=getattr(settings, "OPENROUTER_API_KEY", ""), base_url=getattr(settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"))
    if provider == "vllm":
        base_url = getattr(settings, "VLLM_BASE_URL", "")
        # vLLM may not require a key; OpenAI client needs a non-empty string
        return OpenAI(api_key=getattr(settings, "OPENAI_API_KEY", ""), base_url=base_url)
    # default: openai
    return OpenAI(api_key=getattr(settings, "OPENAI_API_KEY", ""))


def get_model_id(kind: str) -> str:
    if kind == "classify":
        return getattr(settings, "LLM_MODEL_ID_CLASSIFY", getattr(settings, "OPENAI_MODEL_ID_CLASSIFY", "gpt-4"))
    if kind == "chat":
        return getattr(settings, "LLM_MODEL_ID_CHAT", getattr(settings, "OPENAI_MODEL_ID_CHAT", "gpt-4"))
    return getattr(settings, "LLM_MODEL_ID_CHAT", "gpt-4")


