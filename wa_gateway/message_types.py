from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TextEvent:
    sender: str
    text: str
    timestamp: str


@dataclass
class ButtonEvent:
    sender: str
    button_id: str
    text: str
    timestamp: str


@dataclass
class ListEvent:
    sender: str
    list_id: str
    title: str
    timestamp: str


