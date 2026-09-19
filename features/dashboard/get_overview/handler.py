"""Handler agrégats dashboard."""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.dashboard.get_overview.schemas import DashboardOverviewResponse
from infrastructure.database.models.order import Order
from shared.enums import DeliveryStatus
from shared.order_totals import compute_collected_revenue, compute_outstanding_amount


async def handle_get_overview(session: AsyncSession) -> DashboardOverviewResponse:
    """Calcule les indicateurs synthétiques du tableau de bord.

    Contexte:
        Module PDF D — vue d'ensemble CA, impayés, livraisons en attente.

    Comportement:
        1. Charge toutes les commandes (volume back-office modéré).
        2. Pour chaque commande, agrège CA encaissé et impayés via helpers partagés.
        3. Compte commandes ``not_delivered`` ou ``shipping``.

    Règles métier:
        - CA encaissé : ``compute_collected_revenue`` (paid = total, deposit = acompte).
        - Impayés : ``compute_outstanding_amount``.

    Args:
        session: Session async.

    Returns:
        DashboardOverviewResponse: Agrégats.

    Raises:
        N/A

    Effets de bord:
        Lecture seule.

    Voir aussi:
        ``shared.order_totals``.
    """
    result = await session.execute(select(Order))
    orders = result.scalars().all()

    collected = Decimal("0")
    outstanding = Decimal("0")
    pending_delivery = 0

    for order in orders:
        collected += compute_collected_revenue(
            order.total_amount, order.payment_status, order.deposit_amount
        )
        outstanding += compute_outstanding_amount(
            order.total_amount, order.payment_status, order.deposit_amount
        )
        if order.delivery_status in (
            DeliveryStatus.NOT_DELIVERED,
            DeliveryStatus.SHIPPING,
        ):
            pending_delivery += 1

    count_result = await session.execute(select(func.count()).select_from(Order))
    order_count = count_result.scalar_one()

    return DashboardOverviewResponse(
        collected_revenue=collected.quantize(Decimal("0.01")),
        outstanding_amount=outstanding.quantize(Decimal("0.01")),
        pending_delivery_count=pending_delivery,
        order_count=order_count,
    )
