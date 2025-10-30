from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from typing import Iterable

from django.db import transaction
from django.utils import timezone

from inventory.models import Product
from users.models import Customer
from .models import Cart, CartItem, Order, ShippingOption


@dataclass
class CartTotal:
    items_total: Decimal
    shipping_fee: Decimal
    payment_fee: Decimal
    grand_total: Decimal


def _get_active_cart(customer: Customer) -> Cart:
    cart, _ = Cart.objects.get_or_create(customer=customer, is_active=True)
    return cart


def add_to_cart(customer: Customer, product: Product, quantity: int = 1) -> CartItem:
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if product.stock < quantity:
        raise ValueError("Insufficient stock")
    cart = _get_active_cart(customer)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
    if not created:
        new_qty = item.quantity + quantity
        if product.stock < new_qty:
            raise ValueError("Insufficient stock")
        item.quantity = new_qty
        item.save(update_fields=["quantity"])
    return item


def update_quantity(customer: Customer, product: Product, quantity: int) -> CartItem:
    if quantity <= 0:
        return remove_from_cart(customer, product)
    cart = _get_active_cart(customer)
    item = CartItem.objects.get(cart=cart, product=product)
    if product.stock < quantity:
        raise ValueError("Insufficient stock")
    item.quantity = quantity
    item.save(update_fields=["quantity"])
    return item


def remove_from_cart(customer: Customer, product: Product) -> CartItem | None:
    cart = _get_active_cart(customer)
    try:
        item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return None
    item.delete()
    return None


def calculate_total(
    items: Iterable[CartItem], shipping: ShippingOption | None = None, payment_fee: Decimal = Decimal("0.00")
) -> CartTotal:
    items_total = Decimal("0.00")
    for item in items:
        items_total += (item.product.base_price * item.quantity)
    shipping_fee = shipping.price if shipping else Decimal("0.00")
    grand_total = items_total + shipping_fee + payment_fee
    return CartTotal(items_total=items_total, shipping_fee=shipping_fee, payment_fee=payment_fee, grand_total=grand_total)


def get_last_order(customer: Customer) -> Order | None:
    return Order.objects.filter(customer=customer).order_by("-created_at").first()


@transaction.atomic
def create_order(customer: Customer, shipping: ShippingOption | None = None, payment_option=None) -> Order:
    cart = _get_active_cart(customer)
    items = list(cart.items.select_related("product"))
    if not items:
        raise ValueError("Cart is empty")
    # Reserve stock validation
    for it in items:
        if it.product.stock < it.quantity:
            raise ValueError("Insufficient stock for product")

    from django.conf import settings

    prefix = getattr(settings, "ORDER_NUMBER_PREFIX", "ORD")
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    order_number = f"{prefix}{timestamp}{customer.id}"

    # Include payment fee if provided
    payment_fee = getattr(payment_option, "price", Decimal("0.00")) if payment_option else Decimal("0.00")
    totals = calculate_total(items, shipping=shipping, payment_fee=payment_fee)
    order = Order.objects.create(
        order_number=order_number,
        customer=customer,
        cart=cart,
        shipping_option=shipping,
        payment_option=payment_option,
        total_price=totals.grand_total,
    )
    cart.is_active = False
    cart.save(update_fields=["is_active"])
    return order


@transaction.atomic
def finalize_order(order: Order) -> Order:
    if order.status != Order.Status.PENDING:
        return order
    # decrement stock
    for item in order.cart.items.select_related("product"):
        product = item.product
        if product.stock < item.quantity:
            raise ValueError("Insufficient stock during finalization")
        product.stock -= item.quantity
        product.save(update_fields=["stock"])
    order.status = Order.Status.COMPLETED
    order.completed_at = timezone.now()
    order.save(update_fields=["status", "completed_at"])
    return order


@transaction.atomic
def cancel_order(order: Order) -> Order:
    """
    Cancel an order, restoring stock if the order was completed and refunding payments.
    
    Args:
        order: The order to cancel.
        
    Returns:
        The cancelled order.
    """
    if order.status == Order.Status.CANCELLED:
        return order
    
    # If order was COMPLETED, restore stock
    if order.status == Order.Status.COMPLETED:
        for item in order.cart.items.select_related("product"):
            product = item.product
            product.stock += item.quantity
            product.save(update_fields=["stock"])
    
    # Refund any successful payments
    for payment in order.payments.filter(status="success"):
        try:
            payment.refund(reason="Order cancellation")
        except Exception:
            # Log error but continue with cancellation
            pass
    
    order.status = Order.Status.CANCELLED
    order.save(update_fields=["status"])
    return order


def check_abandoned_carts(days: int) -> int:
    threshold = timezone.now() - timedelta(days=days)
    qs = Cart.objects.filter(is_active=True, updated_at__lt=threshold)
    count = qs.count()
    qs.update(is_active=False)
    return count


