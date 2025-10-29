from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
from django.conf import settings

from .embedder import bytes_to_numpy, encode_texts, numpy_to_bytes
from .models import ProductEmbedding, Recommendation, RecommendationProduct


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-8)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-8)
    return np.dot(a_norm, b_norm.T)


def recommend_products(query: str, language: str = "en", top_k: int | None = None) -> Recommendation:
    top_k = top_k or getattr(settings, "RECOS_TOPK", 5)
    threshold = getattr(settings, "DIST_REF_AR" if language == "ar" else "DIST_REF_EN", 0.7)

    # Prepare query embedding
    q_emb = encode_texts([query], language=language)
    q_bytes = numpy_to_bytes(q_emb.astype(np.float32))

    # Load all embeddings for the language
    items = list(ProductEmbedding.objects.filter(language=language).select_related("product"))
    if not items:
        rec = Recommendation.objects.create(customer_input=query, embedding=q_bytes)
        return rec
    mat = np.vstack([bytes_to_numpy(pe.embedding, q_emb.shape[1]).reshape(1, -1) for pe in items])
    sims = cosine_similarity(q_emb, mat)[0]

    ranked_idx = np.argsort(-sims)
    rec = Recommendation.objects.create(customer_input=query, embedding=q_bytes)
    added = 0
    for rank, idx in enumerate(ranked_idx):
        score = float(sims[idx])
        if score < threshold:
            continue
        RecommendationProduct.objects.create(
            recommendation=rec, product_embedding=items[int(idx)], score=score, rank=rank
        )
        added += 1
        if added >= top_k:
            break
    return rec


