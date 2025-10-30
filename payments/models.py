from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from orders.models import Order
from users.models import Customer


class PaymentOptions(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_option = models.ForeignKey(PaymentOptions, on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Payment {self.id} - {self.status}"

    @transaction.atomic
    def capture(self) -> None:
        """
        Capture payment for the order.
        
        This method handles payment capture through the configured payment gateway.
        It validates the payment state, processes the capture, updates payment status,
        and updates the associated order status to PAID upon successful capture.
        
        Raises:
            ValueError: If payment is not in PENDING status or if order is already paid/cancelled.
            RuntimeError: If payment capture fails at the gateway level.
        """
        if self.status != self.Status.PENDING:
            raise ValueError(f"Cannot capture payment with status: {self.status}")
        
        if self.order.status in {Order.Status.PAID, Order.Status.CANCELLED, Order.Status.COMPLETED}:
            raise ValueError(f"Order {self.order.order_number} cannot be paid (status: {self.order.status})")
        
        # Gateway integration hook
        # In production, this would call the actual payment gateway API
        # For now, we'll simulate the capture process
        try:
            # Extract gateway configuration from payment_option
            gateway_url = self.payment_option.url
            
            # Simulate gateway call
            # In production: response = call_payment_gateway_capture(url, transaction_id, amount)
            # For stub implementation, we'll mark as successful if URL is configured
            if gateway_url or getattr(settings, "PAYMENT_GATEWAY_SKIP_VALIDATION", False):
                # Generate transaction ID if not present
                if not self.transaction_id:
                    from django.conf import settings
                    prefix = getattr(settings, "ORDER_NUMBER_PREFIX", "ORD")
                    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
                    self.transaction_id = f"{prefix}PAY{timestamp}{self.id}"
                
                # Update payment status
                self.status = self.Status.SUCCESS
                self.save(update_fields=["status", "transaction_id"])
                
                # Update order status to PAID
                self.order.status = Order.Status.PAID
                self.order.save(update_fields=["status"])
            else:
                # Gateway not configured, mark as failed
                self.status = self.Status.FAILED
                self.save(update_fields=["status"])
                raise RuntimeError("Payment gateway not configured or unavailable")
        except Exception as e:
            # Mark as failed on any exception
            self.status = self.Status.FAILED
            self.save(update_fields=["status"])
            raise RuntimeError(f"Payment capture failed: {e}") from e

    @transaction.atomic
    def refund(self) -> None:
        """
        Refund payment for the order.
        
        This method handles payment refund through the configured payment gateway.
        It validates the payment state, processes the refund, and updates payment status.
        The order status is not automatically changed here as refunds can be partial.
        
        Raises:
            ValueError: If payment is not in SUCCESS status.
            RuntimeError: If payment refund fails at the gateway level.
        """
        if self.status != self.Status.SUCCESS:
            raise ValueError(f"Cannot refund payment with status: {self.status}")
        
        if not self.transaction_id:
            raise ValueError("Cannot refund payment without transaction ID")
        
        # Gateway integration hook
        # In production, this would call the actual payment gateway API
        try:
            # Extract gateway configuration from payment_option
            gateway_url = self.payment_option.url
            
            # Simulate gateway call
            # In production: response = call_payment_gateway_refund(url, transaction_id, amount)
            # For stub implementation, we'll mark as successful if URL is configured
            if gateway_url or getattr(settings, "PAYMENT_GATEWAY_SKIP_VALIDATION", False):
                # Generate refund transaction ID
                from django.conf import settings
                prefix = getattr(settings, "ORDER_NUMBER_PREFIX", "ORD")
                timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
                refund_txn_id = f"{prefix}REF{timestamp}{self.id}"
                
                # Update payment status to indicate refund
                # Note: In a real implementation, you might want a separate REFUNDED status
                # or create a separate Refund record. For now, we'll keep it as SUCCESS
                # but mark the transaction_id to indicate refund
                self.transaction_id = f"{self.transaction_id}|REFUND:{refund_txn_id}"
                self.save(update_fields=["transaction_id"])
                
                # Optionally update order status if full refund
                # For now, we'll leave order status unchanged as refunds can be partial
            else:
                # Gateway not configured, raise error
                raise RuntimeError("Payment gateway not configured or unavailable")
        except Exception as e:
            raise RuntimeError(f"Payment refund failed: {e}") from e


