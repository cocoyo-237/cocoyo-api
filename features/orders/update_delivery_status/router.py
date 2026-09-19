"""Routes - statut livraison."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from core.exceptions import DomainError, domain_error_to_http
from features.orders.create_order.schemas import OrderResponse
from features.orders.update_delivery_status.handler import handle_update_delivery_status
from features.orders.update_delivery_status.schemas import UpdateDeliveryStatusRequest

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.patch(
    "/{order_id}/delivery-status",
    response_model=OrderResponse,
    summary="Mettre à jour la livraison",
)
async def update_delivery_status(
    order_id: str,
    payload: UpdateDeliveryStatusRequest,
    session: DbSession,
    _user: CurrentUser,
) -> OrderResponse:
    """PATCH statut livraison (JWT). HTTP: 200, 404."""
    try:
        return await handle_update_delivery_status(session, order_id, payload)
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
