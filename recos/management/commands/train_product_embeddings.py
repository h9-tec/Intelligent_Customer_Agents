from __future__ import annotations

from django.core.management.base import BaseCommand

from inventory.models import Product, ProductDescription, ProductName
from recos.embedder import encode_texts, numpy_to_bytes
from recos.models import ProductEmbedding


class Command(BaseCommand):
    help = "Generate embeddings for all products (per language)."

    def handle(self, *args, **options):  # type: ignore[override]
        count = 0
        for language in ("en", "ar"):
            # Create product texts by combining name + description for the language
            for product in Product.objects.filter(is_active=True):
                name = ProductName.objects.filter(product=product, language=language).first()
                desc = ProductDescription.objects.filter(product=product, language=language).first()
                text_parts = [
                    name.name if name else "",
                    desc.description if desc else "",
                    str(product.specifications or ""),
                ]
                product_text = "\n".join([p for p in text_parts if p])
                if not product_text.strip():
                    continue
                emb = encode_texts([product_text], language=language)
                ProductEmbedding.objects.update_or_create(
                    product=product,
                    language=language,
                    defaults={
                        "product_text": product_text,
                        "embedding": numpy_to_bytes(emb.reshape(-1)),
                    },
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f"Generated/updated embeddings: {count}"))


