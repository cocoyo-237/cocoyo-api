"""Handler mise à jour statut livraison."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import OrderNotFoundError
from features.orders._shared import order_to_response
from features.orders.create_order.schemas import OrderResponse
from features.orders.update_delivery_status.schemas import UpdateDeliveryStatusRequest
from infrastructure.database.models.order import Order


async def handle_update_delivery_status(
    session: AsyncSession, order_id: str, payload: UpdateDeliveryStatusRequest
) -> OrderResponse:
    """Met à jour le statut de livraison.

    Contexte:
        Module PDF C — suivi livreurs.

    Args:
        session: Session async.
        order_id: UUID commande.
        payload: Nouveau statut livraison.

    Returns:
        OrderResponse: Commande mise à jour.

    Raises:
        OrderNotFoundError: Commande absente.

    Effets de bord:
        Update ``orders.delivery_status``.

    Voir aussi:
        ``handle_update_payment_status``.
    """
    try:
        oid = uuid.UUID(order_id)
    except ValueError as exc:
        raise OrderNotFoundError(order_id) from exc

    result = await session.execute(
        select(Order).where(Order.id == oid).options(selectinload(Order.lines))
    )
    order = result.scalar_one_or_none()
    if order is None:
        raise OrderNotFoundError(order_id)

    order.delivery_status = payload.delivery_status
    await session.flush()
    await session.refresh(order)
    return order_to_response(order)
