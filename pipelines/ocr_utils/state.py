from typing import Optional, TypedDict


class Doc2JSONState(TypedDict, total=True):
    """Состояние графа маршрутизации документов."""

    markdown_result: str
    route: Optional[str]
    response: Optional[str]
