"""Handler liste clients."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.clients.create_client.schemas import ClientResponse
from features.clients.list_clients.schemas import ClientListResponse
from infrastructure.database.models.client import Client


async def handle_list_clients(
    session: AsyncSession, skip: int = 0, limit: int = 50
) -> ClientListResponse:
    """Liste les clients triés par nom.

    Args:
        session: Session async.
        skip: Offset pagination.
        limit: Taille de page.

    Returns:
        ClientListResponse: Liste et total.

    Raises:
        N/A
    """
    total = (await session.execute(select(func.count()).select_from(Client))).scalar_one()
    result = await session.execute(
        select(Client).order_by(Client.nom).offset(skip).limit(limit)
    )
    clients = result.scalars().all()
    items = [
        ClientResponse(
            id=str(c.id),
            name=c.nom,
            first_name=c.prenom,
            contact=c.telephone,
            shipping_address=c.adresse_expedition,
        )
        for c in clients
    ]
    return ClientListResponse(items=items, total=total)
