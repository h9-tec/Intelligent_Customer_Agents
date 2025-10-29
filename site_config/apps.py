from __future__ import annotations

from django.apps import AppConfig


class SiteConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "site_config"

    def ready(self) -> None:  # pragma: no cover
        # Import signals
        from . import signals  # noqa: F401


