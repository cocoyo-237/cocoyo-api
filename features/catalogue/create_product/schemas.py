"""Schémas produit / article."""

from decimal import Decimal

from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    """Corps ``POST /catalogue/products`` → table ``articles``."""

    name: str = Field(..., min_length=1, max_length=100)
    sale_price: Decimal = Field(..., ge=0, description="prix_vente")
    purchase_price: Decimal = Field(..., ge=0, description="prix_achat")
    colors: list[str] = Field(default_factory=list, description="couleurs_disponibles")
    image_url: str | None = Field(default=None)
    stock_quantity: int = Field(default=0, ge=0, description="quantite_stock")


class ProductResponse(BaseModel):
    """Article catalogue."""

    id: str
    name: str
    sale_price: Decimal
    purchase_price: Decimal
    colors: list[str] = Field(default_factory=list)
    image_url: str | None = None
    stock_quantity: int = 0
    is_active: bool = Field(..., description="Dérivé : stock_quantity > 0")
