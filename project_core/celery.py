from __future__ import annotations

import os
from celery import Celery


def _bool_env(name: str, default: bool = False) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in {"1", "true", "yes", "on"}


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_core.settings.dev")

app = Celery("project_core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Eager mode for tests/dev if requested
if _bool_env("CELERY_TASK_ALWAYS_EAGER", False):
    app.conf.task_always_eager = True
    app.conf.task_eager_propagates = True

# Basic beat schedule hooks (tasks must exist)
app.conf.beat_schedule = {
    "cleanup-abandoned-chats": {
        "task": "conversation_log.tasks.cleanup_abandoned_chats",
        "schedule": 60.0 * 60 * 24,
    },
    "cleanup-abandoned-carts": {
        "task": "orders.tasks.cleanup_abandoned_carts",
        "schedule": 60.0 * 60 * 24,
    },
}


