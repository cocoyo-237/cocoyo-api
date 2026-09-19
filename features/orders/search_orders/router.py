"""Routes - recherche commandes."""

from fastapi import APIRouter, Query

from core.dependencies import CurrentUser, DbSession
from features.orders.list_orders.schemas import OrderListResponse
from features.orders.search_orders.handler import handle_search_orders
from shared.enums import DeliveryStatus, PaymentStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/search", response_model=OrderListResponse, summary="Rechercher commandes")
async def search_orders(
    session: DbSession,
    _user: CurrentUser,
    q: str | None = Query(None, description="Nom client (partiel)"),
    payment_status: PaymentStatus | None = Query(None),
    delivery_status: DeliveryStatus | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> OrderListResponse:
    """Recherche/filtre commandes (JWT). HTTP: 200, 401.

    Note:
        Doit être déclaré avant ``GET /orders/{order_id}`` dans le registry
        ou utiliser un chemin distinct - ici ``/orders/search``.
    """
    return await handle_search_orders(
        session,
        q=q,
        payment_status=payment_status,
        delivery_status=delivery_status,
        skip=skip,
        limit=limit,
    )
