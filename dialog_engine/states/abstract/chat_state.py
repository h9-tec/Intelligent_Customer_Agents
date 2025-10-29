from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from conversation_log.models import Chat
from message_bus.message_types import ButtonsMessage, TextMessage


class BaseChatState(ABC):
    def __init__(self, chat: Chat, event: dict) -> None:
        self.chat = chat
        self.event = event

    @abstractmethod
    def handle(self) -> Iterable[object]:
        raise NotImplementedError

    def create_buttons(self) -> list[dict[str, str]]:
        return []


