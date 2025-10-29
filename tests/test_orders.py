from __future__ import annotations

from decimal import Decimal

import pytest

from orders.utils import add_to_cart, calculate_total


@pytest.mark.django_db
def test_add_to_cart(customer, product):
    item = add_to_cart(customer, product, quantity=2)
    assert item.quantity == 2


@pytest.mark.django_db
def test_calculate_total(customer, product):
    item = add_to_cart(customer, product, quantity=1)
    totals = calculate_total([item])
    assert totals.items_total == Decimal("100")


