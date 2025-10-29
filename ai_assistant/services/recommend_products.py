from __future__ import annotations

from typing import Iterable

from inventory.models import Product
from recos.recommender import recommend_products


def recommend_products_for_query(query: str, language: str = "en") -> list[Product]:
    rec = recommend_products(query, language=language)
    products: list[Product] = [item.product_embedding.product for item in rec.items.select_related("product_embedding__product")]
    return products


