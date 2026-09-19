"""Handler recherche commandes."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from features.orders._shared import commande_to_response
from features.orders.list_orders.schemas import OrderListResponse
from infrastructure.database.models.client import Client
from infrastructure.database.models.commande import Commande
from shared.enums import StatutLivraison, StatutPaiement


async def handle_search_orders(
    session: AsyncSession,
    q: str | None = None,
    payment_status: StatutPaiement | None = None,
    delivery_status: StatutLivraison | None = None,
    skip: int = 0,
    limit: int = 50,
) -> OrderListResponse:
    """Recherche par ``clients.nom`` et filtres statuts.

    Args:
        session: Session SQLAlchemy async.

    Returns:
        Réponse du cas d''usage (DTO).

    Raises:
        Voir exceptions domaine propagées.
    """
    stmt = select(Commande).join(Client, Commande.client_id == Client.id)
    if q:
        stmt = stmt.where(Client.nom.ilike(f"%{q}%"))
    if payment_status is not None:
        stmt = stmt.where(Commande.statut_paiement == payment_status)
    if delivery_status is not None:
        stmt = stmt.where(Commande.statut_livraison == delivery_status)

    stmt = (
        stmt.options(selectinload(Commande.lignes))
        .order_by(Commande.date_commande.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    commandes = result.scalars().unique().all()
    return OrderListResponse(
        items=[commande_to_response(c) for c in commandes],
        total=len(commandes),
    )
