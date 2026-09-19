"""Handler détail commande."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import OrderNotFoundError
from features.orders._shared import commande_to_response
from features.orders.create_order.schemas import OrderResponse
from infrastructure.database.models.commande import Commande


async def handle_get_order(session: AsyncSession, order_id: str) -> OrderResponse:
    """Retourne une ``commandes`` et ses lignes.

    Args:
        session: Session SQLAlchemy async.

    Returns:
        Réponse du cas d''usage (DTO).

    Raises:
        Voir exceptions domaine propagées.
    """
    try:
        oid = uuid.UUID(order_id)
    except ValueError as exc:
        raise OrderNotFoundError(order_id) from exc

    result = await session.execute(
        select(Commande).where(Commande.id == oid).options(selectinload(Commande.lignes))
    )
    commande = result.scalar_one_or_none()
    if commande is None:
        raise OrderNotFoundError(order_id)
    return commande_to_response(commande)
