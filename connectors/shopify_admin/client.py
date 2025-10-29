from __future__ import annotations

from typing import Any

import requests
from django.conf import settings


class ShopifyAdminClient:
    def __init__(self) -> None:
        self.base_url = settings.SHOPIFY_STORE_URL.rstrip("/")
        self.api_version = settings.SHOPIFY_API_VERSION
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-Shopify-Access-Token": settings.SHOPIFY_ACCESS_TOKEN,
                "Content-Type": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}/admin/api/{self.api_version}/{path.lstrip('/')}"

    def get_products(self, params: dict[str, Any] | None = None) -> dict:
        resp = self.session.get(self._url("products.json"), params=params or {}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_collections(self) -> dict:
        resp = self.session.get(self._url("custom_collections.json"), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_inventory(self, product_id: int) -> dict:
        resp = self.session.get(self._url(f"products/{product_id}.json"), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def create_order(self, payload: dict[str, Any]) -> dict:
        resp = self.session.post(self._url("orders.json"), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_customers(self, params: dict[str, Any] | None = None) -> dict:
        resp = self.session.get(self._url("customers.json"), params=params or {}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def register_webhook(self, topic: str, address: str) -> dict:
        payload = {"webhook": {"topic": topic, "address": address, "format": "json"}}
        resp = self.session.post(self._url("webhooks.json"), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()


