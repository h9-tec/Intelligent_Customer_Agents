from __future__ import annotations

# Ensure settings module is discoverable for Celery workers
from .celery import app as celery_app  # noqa: F401

__all__ = ["celery_app"]

