"""Routes — liste clients."""

from fastapi import APIRouter, Query

from core.dependencies import CurrentUser, DbSession
from features.clients.list_clients.handler import handle_list_clients
from features.clients.list_clients.schemas import ClientListResponse

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("", response_model=ClientListResponse, summary="Lister les clients")
async def list_clients(
    session: DbSession,
    _user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> ClientListResponse:
    """Liste les clients (JWT). HTTP: 200, 401."""
    return await handle_list_clients(session, skip=skip, limit=limit)
