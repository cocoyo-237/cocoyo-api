"""Schémas - tableau de bord."""

from decimal import Decimal

from pydantic import BaseModel, Field


class DashboardOverviewResponse(BaseModel):
    """Indicateurs page d'accueil back-office (Module PDF D)."""

    collected_revenue: Decimal = Field(...,
                                       description="CA encaissé (paid + acomptes)")
    outstanding_amount: Decimal = Field(...,
                                        description="Montant total à recouvrer")
    pending_delivery_count: int = Field(
        ...,
        description="Commandes non livrées ou en expédition",
    )
    order_count: int = Field(..., description="Nombre total de commandes")
