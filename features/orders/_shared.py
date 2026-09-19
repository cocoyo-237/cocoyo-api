"""Helpers partagés entre slices orders."""

from features.orders.create_order.handler import _order_to_response
from features.orders.create_order.schemas import OrderResponse
from infrastructure.database.models.order import Order

__all__ = ["order_to_response", "OrderResponse"]


def order_to_response(order: Order) -> OrderResponse:
    """Expose le mapping ORM → DTO pour les slices orders.

    Args:
        order: Commande avec lignes chargées.

    Returns:
        OrderResponse: DTO API.
    """
    return _order_to_response(order)
