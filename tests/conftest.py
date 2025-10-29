from __future__ import annotations

import pytest
from django.utils import timezone

from users.models import Customer
from brandkit.models import BrandProfile
from inventory.models import Category, Product, ProductName, ProductDescription
from conversation_log.models import Chat


@pytest.fixture
def customer(db) -> Customer:
    return Customer.objects.create(phone="+1234567890", name="Test User")


@pytest.fixture
def product(db) -> Product:
    brand, _ = BrandProfile.objects.get_or_create(name="ElectroMart")
    cat, _ = Category.objects.get_or_create(name="Phones", brand=brand)
    p = Product.objects.create(
        brand=brand,
        sku="TEST-001",
        base_price=100,
        category=cat,
        stock=10,
        manufacturer="Electro",
        model_number="E1",
        specifications={"ram": "4GB"},
    )
    ProductName.objects.create(product=p, name="Electro One", language="en")
    ProductDescription.objects.create(product=p, description="Test phone", language="en")
    return p


@pytest.fixture
def chat(db, customer: Customer) -> Chat:
    return Chat.objects.create(customer=customer, last_message_date=timezone.now())


