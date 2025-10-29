from __future__ import annotations

import pytest

from recos.recommender import recommend_products


@pytest.mark.django_db
def test_recommend_products_no_embeddings():
    rec = recommend_products("test query", language="en", top_k=3)
    assert rec.items.count() == 0


