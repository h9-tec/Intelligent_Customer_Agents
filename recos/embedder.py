from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import numpy as np
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=2)
def _get_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)


def get_model_for_language(language: str) -> SentenceTransformer:
    if language == "ar":
        return _get_model("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return _get_model("sentence-transformers/all-MiniLM-L6-v2")


def encode_texts(texts: Iterable[str], language: str = "en") -> np.ndarray:
    model = get_model_for_language(language)
    embeddings = model.encode(list(texts), convert_to_numpy=True, show_progress_bar=False)
    return embeddings.astype(np.float32)


def numpy_to_bytes(arr: np.ndarray) -> bytes:
    return arr.tobytes()


def bytes_to_numpy(data: bytes, dim: int) -> np.ndarray:
    arr = np.frombuffer(data, dtype=np.float32)
    if dim and arr.size % dim == 0:
        return arr.reshape((-1, dim))
    return arr


