"""Schémas — liste produits."""

from pydantic import BaseModel, Field

from features.catalogue.create_product.schemas import ProductResponse


class ProductListResponse(BaseModel):
    """Liste de produits."""

    items: list[ProductResponse] = Field(default_factory=list)
    total: int = Field(..., description="Nombre total")
