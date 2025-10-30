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


def _extract_translation(product_data: dict[str, Any], field: str, language: str = "ar") -> str | None:
    """
    Extract translation from Shopify product data.
    
    Shopify stores translations in metafields or via the Translation API.
    This function checks common patterns:
    1. Metafields with language-specific keys (e.g., title_ar, description_ar)
    2. Metafields with translation namespace
    3. Translation API response (if available)
    
    Args:
        product_data: The product dictionary from Shopify API
        field: The field name to extract ('title' or 'body_html')
        language: The language code ('ar' for Arabic)
        
    Returns:
        The translated text if found, None otherwise
    """
    metafields = product_data.get("metafields", [])
    if not isinstance(metafields, list):
        metafields = []
    
    # Pattern 1: Check for language-specific metafield keys
    for metafield in metafields:
        if isinstance(metafield, dict):
            key = metafield.get("key", "")
            namespace = metafield.get("namespace", "")
            value = metafield.get("value", "")
            
            # Check for translations namespace
            if namespace == "translations" and language in key.lower():
                if field == "title" and "title" in key.lower():
                    return str(value)
                if field == "body_html" and ("description" in key.lower() or "body" in key.lower()):
                    return str(value)
            
            # Check for direct language suffix
            if f"{field}_{language}" in key.lower():
                return str(value)
    
    # Pattern 2: Check for translation resource references
    # Shopify Translation API stores translations under translations resource
    # This would require additional API calls, but we can check if translations
    # are already embedded in the product data
    translation_key = f"{field}_{language}"
    if translation_key in product_data:
        return product_data.get(translation_key)
    
    return None


def sync_products() -> int:
    """
    Sync products from Shopify to local database with multilingual support.
    
    This function fetches products from Shopify and creates/updates them in the
    local database, including English and Arabic translations if available.
    
    Returns:
        Number of products synced
    """
    client = ShopifyAdminClient()
    data = client.get_products()
    products = data.get("products", [])
    count = 0
    
    for p in products:
        vendor = p.get("vendor", "")
        brand = _get_or_create_brand(vendor)
        collections = p.get("product_type")  # Simplification; real mapping may use custom collections API
        category = _map_category([{"title": collections}] if collections else [], brand)

        sku = (p.get("variants") or [{}])[0].get("sku") or str(p.get("id", ""))
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
        
        # English name and description (always sync)
        english_title = p.get("title", sku)
        english_description = p.get("body_html", "") or ""
        
        ProductName.objects.update_or_create(
            product=product, 
            language="en", 
            defaults={"name": english_title}
        )
        ProductDescription.objects.update_or_create(
            product=product, 
            language="en", 
            defaults={"description": english_description}
        )
        
        # Arabic name and description (if available)
        arabic_title = _extract_translation(p, "title", "ar")
        arabic_description = _extract_translation(p, "body_html", "ar")
        
        # Only create Arabic entries if translations are available
        if arabic_title:
            ProductName.objects.update_or_create(
                product=product,
                language="ar",
                defaults={"name": arabic_title}
            )
        else:
            # Fallback: Use English title if Arabic translation not available
            # This ensures products are accessible in Arabic even without translations
            ProductName.objects.update_or_create(
                product=product,
                language="ar",
                defaults={"name": english_title}
            )
        
        if arabic_description:
            ProductDescription.objects.update_or_create(
                product=product,
                language="ar",
                defaults={"description": arabic_description}
            )
        else:
            # Fallback: Use English description if Arabic translation not available
            ProductDescription.objects.update_or_create(
                product=product,
                language="ar",
                defaults={"description": english_description}
            )
        
        count += 1
    
    return count


