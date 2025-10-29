from __future__ import annotations

import types

import pytest

from intent_classifier.api import classify_intent


class Dummy:
    class Message:
        content = "Recommendation"

    class Choice:
        message = Message()

    choices = [Choice()]


@pytest.mark.django_db
def test_classify_intent(monkeypatch, settings):
    import intent_classifier.api as api

    monkeypatch.setattr(api.client.chat.completions, "create", lambda **kw: Dummy())
    cat = classify_intent("I need a new phone", "en")
    assert cat == "Recommendation"


