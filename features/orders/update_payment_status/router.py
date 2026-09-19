"""Routes - statut paiement."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from core.exceptions import DomainError, domain_error_to_http
from features.orders.create_order.schemas import OrderResponse
from features.orders.update_payment_status.handler import handle_update_payment_status
from features.orders.update_payment_status.schemas import UpdatePaymentStatusRequest

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.patch(
    "/{order_id}/payment-status",
    response_model=OrderResponse,
    summary="Mettre à jour le paiement",
)
async def update_payment_status(
    order_id: str,
    payload: UpdatePaymentStatusRequest,
    session: DbSession,
    _user: CurrentUser,
) -> OrderResponse:
    """PATCH statut paiement (JWT). HTTP: 200, 400, 404."""
    try:
        return await handle_update_payment_status(session, order_id, payload)
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
