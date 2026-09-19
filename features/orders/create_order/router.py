"""Routes - création commande."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from core.exceptions import DomainError, domain_error_to_http
from features.orders.create_order.handler import handle_create_order
from features.orders.create_order.schemas import CreateOrderRequest, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=201, summary="Créer une commande")
async def create_order(
    payload: CreateOrderRequest,
    session: DbSession,
    _user: CurrentUser,
) -> OrderResponse:
    """Crée une commande panier (JWT). HTTP: 201, 404, 422."""
    try:
        return await handle_create_order(session, payload)
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
