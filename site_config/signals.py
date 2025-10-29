from __future__ import annotations

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SiteConfiguration


@receiver(post_save, sender=SiteConfiguration)
def clear_site_config_cache(sender, instance: SiteConfiguration, **kwargs):  # pragma: no cover
    cache.delete(SiteConfiguration._cache_key())


