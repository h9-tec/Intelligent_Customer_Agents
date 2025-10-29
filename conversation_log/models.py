from __future__ import annotations

from django.db import models
from django.utils import timezone

from users.models import Customer


class ConversationState(models.TextChoices):
    IDLE = "idle", "Idle"
    ASSISTANT = "assistant", "Assistant"
    CHECKOUT = "checkout", "Checkout"
    CART = "cart", "Cart"


class MessageType(models.TextChoices):
    TEXT = "text", "Text"
    BUTTON = "button", "Button"
    LIST = "list", "List"


class Chat(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="chats")
    current_state = models.CharField(max_length=64, blank=True, null=True)
    last_message_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    language = models.CharField(max_length=4, default="en")

    def touch(self) -> None:
        self.last_message_date = timezone.now()
        self.save(update_fields=["last_message_date"])


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    response = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=64, blank=True, default="")
    language = models.CharField(max_length=4, default="en")
    tokens = models.IntegerField(default=0)
    type = models.CharField(max_length=16, choices=MessageType.choices, default=MessageType.TEXT)


