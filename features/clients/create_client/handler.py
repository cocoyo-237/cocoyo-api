"""Handler création client."""

from sqlalchemy.ext.asyncio import AsyncSession

from features.clients.create_client.schemas import ClientResponse, CreateClientRequest
from infrastructure.database.models.client import Client


async def handle_create_client(
    session: AsyncSession, payload: CreateClientRequest
) -> ClientResponse:
    """Persiste un nouveau client en base.

    Contexte:
        Module PDF B — prérequis prise de commande.

    Préconditions:
        JWT valide (vérifié au niveau route).

    Comportement:
        1. Instancie ``Client``.
        2. ``session.add`` + ``flush`` pour obtenir l'id.

    Transactions:
        Commit effectué par ``get_async_session`` en fin de requête.

    Args:
        session: Session async.
        payload: Nom et contact.

    Returns:
        ClientResponse: Client créé.

    Raises:
        N/A

    Effets de bord:
        Insert dans ``clients``.

    Exemple:
        >>> # {"name": "Alice", "contact": "+237..."}

    Voir aussi:
        ``features.orders.create_order``.
    """
    client = Client(name=payload.name, contact=payload.contact)
    session.add(client)
    await session.flush()
    await session.refresh(client)
    return ClientResponse(id=str(client.id), name=client.name, contact=client.contact)
