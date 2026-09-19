"""Handler agrégats dashboard."""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from features.dashboard.get_overview.schemas import DashboardOverviewResponse
from features.orders._shared import commande_total
from infrastructure.database.models.commande import Commande
from shared.enums import StatutLivraison
from shared.order_totals import compute_collected_revenue, compute_outstanding_amount


async def handle_get_overview(session: AsyncSession) -> DashboardOverviewResponse:
    """Indicateurs à partir de ``commandes`` et lignes.

    Args:
        session: Session async.

    Returns:
        DashboardOverviewResponse: Agrégats CA, impayés, livraisons.

    Raises:
        N/A
    """
    result = await session.execute(
        select(Commande).options(selectinload(Commande.lignes))
    )
    commandes = result.scalars().all()

    collected = Decimal("0")
    outstanding = Decimal("0")
    pending_delivery = 0

    for commande in commandes:
        total = commande_total(commande)
        collected += compute_collected_revenue(
            total, commande.statut_paiement, commande.montant_avance
        )
        outstanding += compute_outstanding_amount(
            total, commande.statut_paiement, commande.montant_avance
        )
        if commande.statut_livraison in (
            StatutLivraison.NON_LIVRE,
            StatutLivraison.EN_COURS,
        ):
            pending_delivery += 1

    count_result = await session.execute(select(func.count()).select_from(Commande))
    order_count = count_result.scalar_one()

    return DashboardOverviewResponse(
        collected_revenue=collected.quantize(Decimal("0.01")),
        outstanding_amount=outstanding.quantize(Decimal("0.01")),
        pending_delivery_count=pending_delivery,
        order_count=order_count,
    )
