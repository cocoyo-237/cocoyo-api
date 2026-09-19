"""Routes - liste commandes."""

from fastapi import APIRouter, Query

from core.dependencies import CurrentUser, DbSession
from features.orders.list_orders.handler import handle_list_orders
from features.orders.list_orders.schemas import OrderListResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=OrderListResponse, summary="Lister les commandes")
async def list_orders(
    session: DbSession,
    _user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> OrderListResponse:
    """Liste commandes (JWT). HTTP: 200, 401."""
    return await handle_list_orders(session, skip=skip, limit=limit)
