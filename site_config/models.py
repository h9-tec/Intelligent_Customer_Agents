from __future__ import annotations

from django.core.cache import cache
from django.db import models


class SiteConfiguration(models.Model):
    """Singleton configuration for dynamic site settings."""

    language_default = models.CharField(max_length=8, default="en")
    support_email = models.EmailField(blank=True, default="")
    support_phone = models.CharField(max_length=32, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"

    def save(self, *args, **kwargs):  # type: ignore[override]
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(self._cache_key())

    def delete(self, *args, **kwargs):  # type: ignore[override]
        # Prevent deletion; enforce singleton
        raise RuntimeError("Deletion of SiteConfiguration is not allowed")

    @classmethod
    def get_solo(cls) -> "SiteConfiguration":
        cache_key = cls._cache_key()
        obj: SiteConfiguration | None = cache.get(cache_key)
        if obj is None:
            obj, _ = cls.objects.get_or_create(pk=1)
            cache.set(cache_key, obj, 60)
        return obj

    @classmethod
    def _cache_key(cls) -> str:
        return "site_config:singleton"


