from __future__ import annotations

from typing import Any

from brandkit.models import BrandProfile
from inventory.models import Category, Product, ProductDescription, ProductName
from .client import ShopifyAdminClient


def _get_or_create_brand(vendor: str) -> BrandProfile:
    brand, _ = BrandProfile.objects.get_or_create(name=vendor or "Generic")
    return brand


def _map_category(collections: list[dict[str, Any]], brand: BrandProfile) -> Category:
    if not collections:
        cat, _ = Category.objects.get_or_create(name="Uncategorized", brand=brand)
        return cat
    name = collections[0].get("title", "Uncategorized")
    cat, _ = Category.objects.get_or_create(name=name, brand=brand)
    return cat


def sync_products() -> int:
    client = ShopifyAdminClient()
    data = client.get_products()
    products = data.get("products", [])
    count = 0
    for p in products:
        vendor = p.get("vendor", "")
        brand = _get_or_create_brand(vendor)
        collections = p.get("product_type")  # Simplification; real mapping may use custom collections API
        category = _map_category([{"title": collections}] if collections else [], brand)

        sku = (p.get("variants") or [{}])[0].get("sku") or p.get("id")
        base_price = (p.get("variants") or [{}])[0].get("price") or 0
        image_url = (p.get("image") or {}).get("src")
        manufacturer = vendor
        model_number = p.get("handle")
        release_year = None
        specs = {
            "title": p.get("title"),
            "metafields": p.get("metafields", {}),
        }

        product, _ = Product.objects.update_or_create(
            sku=sku,
            defaults={
                "brand": brand,
                "base_price": base_price,
                "category": category,
                "is_active": True,
                "manufacturer": manufacturer,
                "model_number": model_number,
                "release_year": release_year,
                "specifications": specs,
            },
        )
        # Names and descriptions for EN only (stub)
        ProductName.objects.update_or_create(product=product, language="en", defaults={"name": p.get("title", sku)})
        ProductDescription.objects.update_or_create(
            product=product, language="en", defaults={"description": p.get("body_html", "")} 
        )
        count += 1
    return count


