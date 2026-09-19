"""Schémas - mise à jour article."""

from decimal import Decimal

from pydantic import BaseModel, Field


class UpdateProductRequest(BaseModel):
    """Corps ``PATCH /catalogue/products/{id}``."""

    name: str | None = Field(default=None, max_length=100)
    sale_price: Decimal | None = Field(default=None, ge=0)
    purchase_price: Decimal | None = Field(default=None, ge=0)
    colors: list[str] | None = Field(default=None)
    image_url: str | None = Field(default=None)
    stock_quantity: int | None = Field(default=None, ge=0)
