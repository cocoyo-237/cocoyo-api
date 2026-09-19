"""Schémas - statut paiement."""

from decimal import Decimal

from pydantic import BaseModel, Field

from shared.enums import PaymentStatus


class UpdatePaymentStatusRequest(BaseModel):
    """Corps ``PATCH /orders/{id}/payment-status``."""

    payment_status: PaymentStatus = Field(...,
                                          description="Nouveau statut paiement")
    deposit_amount: Decimal | None = Field(
        default=None,
        ge=0,
        description="Montant acompte si statut deposit",
    )
