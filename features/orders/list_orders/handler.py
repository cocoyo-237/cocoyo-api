"""Handler liste commandes."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from features.orders._shared import order_to_response
from features.orders.list_orders.schemas import OrderListResponse
from infrastructure.database.models.order import Order


async def handle_list_orders(
    session: AsyncSession, skip: int = 0, limit: int = 50
) -> OrderListResponse:
    """Liste les commandes par date décroissante.

    Contexte:
        Module PDF B/C — suivi commandes.

    Args:
        session: Session async.
        skip: Offset.
        limit: Page size.

    Returns:
        OrderListResponse: Commandes avec lignes.

    Raises:
        N/A

    Effets de bord:
        Lecture seule.

    Voir aussi:
        ``handle_get_order``.
    """
    total = (await session.execute(select(func.count()).select_from(Order))).scalar_one()
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.lines))
        .order_by(Order.ordered_at.desc())
        .offset(skip)
        .limit(limit)
    )
    orders = result.scalars().all()
    return OrderListResponse(
        items=[order_to_response(o) for o in orders],
        total=total,
    )
