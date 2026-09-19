"""Handler liste commandes."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from features.orders._shared import commande_to_response
from features.orders.list_orders.schemas import OrderListResponse
from infrastructure.database.models.commande import Commande


async def handle_list_orders(
    session: AsyncSession, skip: int = 0, limit: int = 50
) -> OrderListResponse:
    """Liste ``commandes`` par date décroissante.

    Args:
        session: Session async.
        skip: Offset.
        limit: Page size.

    Returns:
        OrderListResponse: Commandes paginées.

    Raises:
        N/A
    """
    total = (await session.execute(select(func.count()).select_from(Commande))).scalar_one()
    result = await session.execute(
        select(Commande)
        .options(selectinload(Commande.lignes))
        .order_by(Commande.date_commande.desc())
        .offset(skip)
        .limit(limit)
    )
    commandes = result.scalars().all()
    return OrderListResponse(
        items=[commande_to_response(c) for c in commandes],
        total=total,
    )
