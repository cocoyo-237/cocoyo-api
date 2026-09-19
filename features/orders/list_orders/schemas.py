"""Schémas — liste commandes."""

from pydantic import BaseModel, Field

from features.orders.create_order.schemas import OrderResponse


class OrderListResponse(BaseModel):
    """Liste commandes."""

    items: list[OrderResponse] = Field(default_factory=list)
    total: int = Field(..., description="Total commandes")
