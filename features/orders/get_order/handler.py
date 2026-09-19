"""Handler détail commande."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import OrderNotFoundError
from features.orders._shared import order_to_response
from features.orders.create_order.schemas import OrderResponse
from infrastructure.database.models.order import Order


async def handle_get_order(session: AsyncSession, order_id: str) -> OrderResponse:
    """Retourne une commande et ses lignes.

    Contexte:
        Module PDF B — détail commande.

    Args:
        session: Session async.
        order_id: UUID commande.

    Returns:
        OrderResponse: Commande complète.

    Raises:
        OrderNotFoundError: Commande absente.

    Effets de bord:
        Lecture seule.

    Voir aussi:
        ``handle_list_orders``.
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
    return order_to_response(order)
