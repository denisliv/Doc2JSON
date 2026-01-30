"""
Pydantic-модель ответа роутера: категория документа.
"""

from typing import Literal

from pydantic import BaseModel, Field

RouterRoute = Literal["accounting_statements", "official_request", "other"]


class RouterResponseModel(BaseModel):
    """Ответ классификатора документов: один из трёх маршрутов."""

    route: RouterRoute = Field(
        ...,
        description="Категория документа: accounting_statements, official_request или other",
    )
