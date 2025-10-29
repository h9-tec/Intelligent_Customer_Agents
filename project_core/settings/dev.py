from __future__ import annotations

from .base import *  # noqa: F401,F403

import os

DEBUG = True

# Load .env if present (only in dev)
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover
    pass

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


