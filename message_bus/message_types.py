from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence


@dataclass
class TextMessage:
    to: str
    text: str


@dataclass
class Button:
    id: str
    title: str


@dataclass
class ButtonsMessage:
    to: str
    body: str
    buttons: Sequence[Button]


@dataclass
class ListMessage:
    to: str
    header: str
    title: str
    sections: Sequence[dict[str, Any]]


@dataclass
class ImageMessage:
    to: str
    image_url: str
    caption: str | None = None


@dataclass
class ProductMessage:
    to: str
    product_id: int
    title: str
    price: str
    image_url: str | None = None


@dataclass
class ProductListMessage:
    to: str
    products: Sequence[dict[str, Any]]  # [{id, title, price, image_url}]
    header: str | None = None
    body: str | None = None


@dataclass
class CartMessage:
    to: str
    items: Sequence[dict[str, Any]]  # [{name, qty, price, subtotal}]
    total: str

