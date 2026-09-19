"""Schémas Pydantic partagés - commandes (évite imports circulaires)."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from shared.enums import StatutLivraison, StatutPaiement


class OrderLineRequest(BaseModel):
    """Ligne panier."""

    product_id: str = Field(..., description="UUID article")
    size: str = Field(..., min_length=1, description="Couleur choisie")
    quantity: int = Field(..., gt=0)


class CreateOrderRequest(BaseModel):
    """Corps création commande."""

    client_id: str = Field(..., description="UUID client")
    lines: list[OrderLineRequest] = Field(..., min_length=1)
    lieu_livraison: str | None = Field(default=None)
    reduction: Decimal = Field(default=Decimal("0"), ge=0)


class OrderLineResponse(BaseModel):
    """Ligne commande API."""

    product_id: str
    size: str
    quantity: int
    unit_price: Decimal
    unit_cost: Decimal


class OrderResponse(BaseModel):
    """Commande API."""

    id: str
    client_id: str
    ordered_at: datetime | None
    payment_status: StatutPaiement | None
    delivery_status: StatutLivraison | None
    total_amount: Decimal
    deposit_amount: Decimal
    reduction: Decimal = Decimal("0")
    lieu_livraison: str | None = None
    lines: list[OrderLineResponse] = Field(default_factory=list)
