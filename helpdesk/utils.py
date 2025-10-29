from __future__ import annotations

from typing import Sequence

import numpy as np

from recos.embedder import bytes_to_numpy, encode_texts
from .models import Faq, FaqEmbedding


def recommend_faqs(query: str, language: str = "en", top_k: int = 3, threshold: float | None = None) -> list[Faq]:
    if threshold is None:
        threshold = 0.7 if language == "en" else 0.75
    q_emb = encode_texts([query], language=language)
    entries = list(FaqEmbedding.objects.filter(faq__language=language, faq__is_active=True).select_related("faq"))
    if not entries:
        return []
    mat = np.vstack([bytes_to_numpy(e.embedding, q_emb.shape[1]).reshape(1, -1) for e in entries])
    sims = (q_emb / (np.linalg.norm(q_emb) + 1e-8)) @ (mat.T / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-8))
    sims = sims.flatten()
    ranked_idx = np.argsort(-sims)
    results: list[Faq] = []
    for idx in ranked_idx[:top_k * 2]:  # evaluate more then filter by threshold
        score = float(sims[int(idx)])
        if score < threshold:
            continue
        results.append(entries[int(idx)].faq)
        if len(results) >= top_k:
            break
    return results


