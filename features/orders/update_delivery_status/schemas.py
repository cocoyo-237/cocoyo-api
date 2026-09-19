"""Schémas — statut livraison."""

from pydantic import BaseModel, Field

from shared.enums import DeliveryStatus


class UpdateDeliveryStatusRequest(BaseModel):
    """Corps ``PATCH /orders/{id}/delivery-status``."""

    delivery_status: DeliveryStatus = Field(..., description="Nouveau statut livraison")
