"""Handler mise à jour statut livraison."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import OrderNotFoundError
from features.orders._shared import commande_to_response
from features.orders.create_order.schemas import OrderResponse
from features.orders.update_delivery_status.schemas import UpdateDeliveryStatusRequest
from infrastructure.database.models.commande import Commande


async def handle_update_delivery_status(
    session: AsyncSession, order_id: str, payload: UpdateDeliveryStatusRequest
) -> OrderResponse:
    """Met à jour ``statut_livraison``.

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

    commande.statut_livraison = payload.delivery_status
    await session.flush()
    await session.refresh(commande)
    return commande_to_response(commande)
