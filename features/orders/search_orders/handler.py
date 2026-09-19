"""Handler recherche commandes."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from features.orders._shared import order_to_response
from features.orders.list_orders.schemas import OrderListResponse
from infrastructure.database.models.client import Client
from infrastructure.database.models.order import Order
from shared.enums import DeliveryStatus, PaymentStatus


async def handle_search_orders(
    session: AsyncSession,
    q: str | None = None,
    payment_status: PaymentStatus | None = None,
    delivery_status: DeliveryStatus | None = None,
    skip: int = 0,
    limit: int = 50,
) -> OrderListResponse:
    """Recherche commandes par nom client et/ou statuts.

    Contexte:
        Module PDF D — filtres et recherche.

    Comportement:
        1. Joint ``clients`` si ``q`` fourni (ILIKE sur name).
        2. Filtre statuts optionnels.
        3. Retourne page paginée.

    Args:
        session: Session async.
        q: Fragment nom client.
        payment_status: Filtre paiement.
        delivery_status: Filtre livraison.
        skip: Offset.
        limit: Taille page.

    Returns:
        OrderListResponse: Résultats (total = taille page filtrée simplifiée).

    Raises:
        N/A

    Effets de bord:
        Lecture seule.

    Voir aussi:
        ``handle_get_overview``.
    """
    stmt = select(Order).join(Client, Order.client_id == Client.id)
    if q:
        stmt = stmt.where(Client.name.ilike(f"%{q}%"))
    if payment_status is not None:
        stmt = stmt.where(Order.payment_status == payment_status)
    if delivery_status is not None:
        stmt = stmt.where(Order.delivery_status == delivery_status)

    stmt = (
        stmt.options(selectinload(Order.lines))
        .order_by(Order.ordered_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    orders = result.scalars().unique().all()
    return OrderListResponse(
        items=[order_to_response(o) for o in orders],
        total=len(orders),
    )
