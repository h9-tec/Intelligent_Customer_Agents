from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hook/", include("wa_gateway.urls")),
    path("api/", include("api.urls")),
]


