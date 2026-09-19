"""Handler mise à jour statut paiement."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import DomainError, OrderNotFoundError
from features.orders._shared import commande_to_response, commande_total
from features.orders.create_order.schemas import OrderResponse
from features.orders.update_payment_status.schemas import UpdatePaymentStatusRequest
from infrastructure.database.models.commande import Commande
from shared.enums import StatutPaiement


async def handle_update_payment_status(
    session: AsyncSession, order_id: str, payload: UpdatePaymentStatusRequest
) -> OrderResponse:
    """Met à jour ``statut_paiement`` et ``montant_avance``.

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

    total = commande_total(commande)

    if payload.payment_status == StatutPaiement.AVANCE_PAYEE:
        if payload.deposit_amount is None:
            raise DomainError("deposit_amount est requis pour le statut avance_payee")
        if payload.deposit_amount > total:
            raise DomainError("L'acompte ne peut pas dépasser le total")
        commande.montant_avance = payload.deposit_amount
    elif payload.payment_status == StatutPaiement.PAYE_INTEGRALEMENT:
        commande.montant_avance = total
    elif payload.payment_status == StatutPaiement.EN_ATTENTE:
        commande.montant_avance = Decimal("0")

    commande.statut_paiement = payload.payment_status
    await session.flush()
    await session.refresh(commande)
    return commande_to_response(commande)
