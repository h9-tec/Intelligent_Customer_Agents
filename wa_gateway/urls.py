from __future__ import annotations

from django.urls import path

from .views import WebhookMessageView, WebhookVerifyView


urlpatterns = [
    path("", WebhookMessageView.as_view(), name="wa-webhook"),
    path("verify/", WebhookVerifyView.as_view(), name="wa-verify"),
]


