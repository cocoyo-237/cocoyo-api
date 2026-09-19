"""Routes - création client."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from features.clients.create_client.handler import handle_create_client
from features.clients.create_client.schemas import ClientResponse, CreateClientRequest

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("", response_model=ClientResponse, status_code=201, summary="Créer un client")
async def create_client(
    payload: CreateClientRequest,
    session: DbSession,
    _user: CurrentUser,
) -> ClientResponse:
    """Crée un client (JWT requis). HTTP: 201, 401, 422."""
    return await handle_create_client(session, payload)
