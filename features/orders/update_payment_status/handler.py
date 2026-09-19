"""Handler mise à jour statut paiement."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import DomainError, OrderNotFoundError
from features.orders._shared import order_to_response
from features.orders.create_order.schemas import OrderResponse
from features.orders.update_payment_status.schemas import UpdatePaymentStatusRequest
from infrastructure.database.models.order import Order
from shared.enums import PaymentStatus


async def handle_update_payment_status(
    session: AsyncSession, order_id: str, payload: UpdatePaymentStatusRequest
) -> OrderResponse:
    """Met à jour le statut de paiement d'une commande.

    Contexte:
        Module PDF C — suivi paiements.

    Règles métier:
        - Si ``deposit``, ``deposit_amount`` obligatoire et <= ``total_amount``.
        - Si ``paid``, ``deposit_amount`` forcé à ``total_amount``.

    Args:
        session: Session async.
        order_id: UUID commande.
        payload: Nouveau statut et acompte optionnel.

    Returns:
        OrderResponse: Commande mise à jour.

    Raises:
        OrderNotFoundError: Commande absente.
        DomainError: Acompte invalide.

    Effets de bord:
        Update ``orders.payment_status`` et ``deposit_amount``.

    Voir aussi:
        ``handle_update_delivery_status``.
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

    if payload.payment_status == PaymentStatus.DEPOSIT:
        if payload.deposit_amount is None:
            raise DomainError("deposit_amount est requis pour le statut deposit")
        if payload.deposit_amount > order.total_amount:
            raise DomainError("L'acompte ne peut pas dépasser le total")
        order.deposit_amount = payload.deposit_amount
    elif payload.payment_status == PaymentStatus.PAID:
        order.deposit_amount = order.total_amount
    elif payload.payment_status == PaymentStatus.UNPAID:
        order.deposit_amount = Decimal("0")

    order.payment_status = payload.payment_status
    await session.flush()
    await session.refresh(order)
    return order_to_response(order)
