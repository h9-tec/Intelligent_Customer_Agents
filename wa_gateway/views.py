from __future__ import annotations

import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.views import APIView

from .tasks import process_inbound_message


class WebhookVerifyView(APIView):
    authentication_classes: list[Any] = []
    permission_classes: list[Any] = []

    def get(self, request: HttpRequest) -> HttpResponse:  # type: ignore[override]
        verify_token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge", "")
        if verify_token == getattr(settings, "WA_VERIFY_TOKEN", ""):
            return HttpResponse(challenge)
        return HttpResponse("Invalid token", status=403)


class WebhookMessageView(APIView):
    authentication_classes: list[Any] = []
    permission_classes: list[Any] = []

    def post(self, request: HttpRequest) -> JsonResponse:  # type: ignore[override]
        payload = request.data or {}
        entries = payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                for message in messages:
                    sender = message.get("from")
                    timestamp = message.get("timestamp")
                    event_data: dict[str, Any] = {"sender": sender, "timestamp": timestamp}
                    if message.get("type") == "text":
                        event_data["text"] = message.get("text", {}).get("body", "")
                        event_data["event_type"] = "text"
                    elif message.get("type") == "interactive":
                        interactive = message.get("interactive", {})
                        if interactive.get("type") == "button_reply":
                            event_data["event_type"] = "button"
                            event_data["button_id"] = interactive.get("button_reply", {}).get("id", "")
                            event_data["text"] = interactive.get("button_reply", {}).get("title", "")
                        elif interactive.get("type") == "list_reply":
                            event_data["event_type"] = "list"
                            event_data["list_id"] = interactive.get("list_reply", {}).get("id", "")
                            event_data["title"] = interactive.get("list_reply", {}).get("title", "")
                    else:
                        continue
                    process_inbound_message.delay(event_data)
        return JsonResponse({"status": "ok"})


