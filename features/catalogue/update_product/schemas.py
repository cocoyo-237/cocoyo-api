"""Schémas — mise à jour produit."""

from decimal import Decimal

from pydantic import BaseModel, Field

from features.catalogue.create_product.schemas import ProductResponse


class UpdateProductRequest(BaseModel):
    """Corps ``PATCH /catalogue/products/{id}``."""

    name: str | None = Field(default=None, description="Nouveau nom")
    category: str | None = Field(default=None, description="Nouvelle catégorie")
    sizes: list[str] | None = Field(default=None, description="Nouvelles tailles")
    unit_price: Decimal | None = Field(default=None, ge=0, description="Nouveau prix")
