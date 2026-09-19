"""Routes - détail commande."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from core.exceptions import DomainError, domain_error_to_http
from features.orders.create_order.schemas import OrderResponse
from features.orders.get_order.handler import handle_get_order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/{order_id}", response_model=OrderResponse, summary="Détail commande")
async def get_order(
    order_id: str,
    session: DbSession,
    _user: CurrentUser,
) -> OrderResponse:
    """GET commande par id (JWT). HTTP: 200, 404."""
    try:
        return await handle_get_order(session, order_id)
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
