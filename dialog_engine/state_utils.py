from __future__ import annotations

from typing import Tuple


def parse_button_id(button_id: str) -> tuple[str, list[str]]:
    """Parse button id like Prefix_arg1_arg2... → (Prefix, [args]).

    If no underscore present, returns (button_id, []).
    """
    if not button_id:
        return "", []
    parts = button_id.split("_")
    if len(parts) == 1:
        return parts[0], []
    return parts[0], parts[1:]


