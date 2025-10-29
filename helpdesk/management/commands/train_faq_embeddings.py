from __future__ import annotations

from django.core.management.base import BaseCommand

from helpdesk.models import Faq, FaqEmbedding
from recos.embedder import encode_texts, numpy_to_bytes


class Command(BaseCommand):
    help = "Generate embeddings for FAQs"

    def handle(self, *args, **options):  # type: ignore[override]
        count = 0
        for faq in Faq.objects.filter(is_active=True):
            emb = encode_texts([faq.question + "\n" + faq.answer], language=faq.language)
            FaqEmbedding.objects.update_or_create(
                faq=faq,
                defaults={"embedding": numpy_to_bytes(emb.reshape(-1))},
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Generated/updated FAQ embeddings: {count}"))


