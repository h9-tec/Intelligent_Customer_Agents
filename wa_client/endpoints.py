from __future__ import annotations


def base_url(version: str = "v16.0") -> str:
    return f"https://graph.facebook.com/{version}"


def messages_url(phone_id: str, version: str = "v16.0") -> str:
    return f"{base_url(version)}/{phone_id}/messages"


def mark_read_url(message_id: str, version: str = "v16.0") -> str:
    # Mark read uses the same messages endpoint with status payload
    return ""


