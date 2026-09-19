"""Schémas — création commande."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from shared.enums import DeliveryStatus, PaymentStatus


class OrderLineRequest(BaseModel):
    """Ligne panier pour création commande."""

    product_id: str = Field(..., description="UUID produit catalogue")
    size: str = Field(..., min_length=1, description="Taille commandée")
    quantity: int = Field(..., gt=0, description="Quantité")


class CreateOrderRequest(BaseModel):
    """Corps ``POST /orders``."""

    client_id: str = Field(..., description="UUID client")
    lines: list[OrderLineRequest] = Field(..., min_length=1, description="Articles du panier")


class OrderLineResponse(BaseModel):
    """Ligne persistée."""

    product_id: str = Field(..., description="UUID produit")
    size: str = Field(..., description="Taille")
    quantity: int = Field(..., description="Quantité")
    unit_price: Decimal = Field(..., description="Prix unitaire figé")


class OrderResponse(BaseModel):
    """Commande complète."""

    id: str = Field(..., description="UUID commande")
    client_id: str = Field(..., description="UUID client")
    ordered_at: datetime = Field(..., description="Date commande")
    payment_status: PaymentStatus = Field(..., description="Statut paiement")
    delivery_status: DeliveryStatus = Field(..., description="Statut livraison")
    total_amount: Decimal = Field(..., description="Montant total")
    deposit_amount: Decimal = Field(..., description="Acompte enregistré")
    lines: list[OrderLineResponse] = Field(default_factory=list, description="Lignes")
