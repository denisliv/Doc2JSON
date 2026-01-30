"""
Типы состояния графа маршрутизации документов Doc2JSON.
"""

from typing import Optional, TypedDict


class Doc2JSONState(TypedDict):
    """Состояние графа маршрутизации документов."""

    markdown_result: str
    route: Optional[str]
    response: Optional[str]
