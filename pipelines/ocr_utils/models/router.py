"""
Pydantic-модель ответа роутера: категория документа.
"""

from typing import Literal

from pydantic import BaseModel, Field


class RouterResponseModel(BaseModel):
    route: Literal["accounting_statements", "official_request", "other"] = Field(
        ...,
        description="Категория документа: accounting_statements, official_request или other",
    )
