from __future__ import annotations

from django.contrib import admin

from .models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("language_default", "support_email", "support_phone", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):  # type: ignore[override]
        # Only allow adding if it doesn't exist
        exists = SiteConfiguration.objects.exists()
        return not exists


