"""Handler liste clients."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.clients.create_client.schemas import ClientResponse
from features.clients.list_clients.schemas import ClientListResponse
from infrastructure.database.models.client import Client


async def handle_list_clients(
    session: AsyncSession, skip: int = 0, limit: int = 50
) -> ClientListResponse:
    """Retourne les clients triés par nom.

    Contexte:
        Module PDF B — sélection client pour commande.

    Préconditions:
        JWT valide.

    Args:
        session: Session async.
        skip: Offset pagination.
        limit: Taille page (max 100 côté route).

    Returns:
        ClientListResponse: Items et total.

    Raises:
        N/A

    Effets de bord:
        Lecture seule.

    Exemple:
        >>> await handle_list_clients(session, skip=0, limit=20)

    Voir aussi:
        ``handle_create_client``.
    """
    count_result = await session.execute(select(func.count()).select_from(Client))
    total = count_result.scalar_one()
    result = await session.execute(
        select(Client).order_by(Client.name).offset(skip).limit(limit)
    )
    clients = result.scalars().all()
    items = [
        ClientResponse(id=str(c.id), name=c.name, contact=c.contact) for c in clients
    ]
    return ClientListResponse(items=items, total=total)
