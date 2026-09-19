"""Schémas produit — création."""

from decimal import Decimal

from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    """Corps ``POST /catalogue/products`` (Module PDF A)."""

    name: str = Field(..., min_length=1, max_length=255, description="Nom du vêtement")
    category: str = Field(..., min_length=1, description="Catégorie (ex. Robe, T-shirt)")
    sizes: list[str] = Field(..., min_length=1, description="Tailles disponibles")
    unit_price: Decimal = Field(..., ge=0, description="Prix unitaire", examples=["15000.00"])


class ProductResponse(BaseModel):
    """Produit catalogue."""

    id: str = Field(..., description="UUID produit")
    name: str = Field(..., description="Nom")
    category: str = Field(..., description="Catégorie")
    sizes: list[str] = Field(..., description="Tailles")
    unit_price: Decimal = Field(..., description="Prix unitaire")
    is_active: bool = Field(..., description="Actif si true")
