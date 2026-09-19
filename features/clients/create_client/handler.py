"""Handler création client."""

from sqlalchemy.ext.asyncio import AsyncSession

from features.clients.create_client.schemas import ClientResponse, CreateClientRequest
from infrastructure.database.models.client import Client


async def handle_create_client(
    session: AsyncSession, payload: CreateClientRequest
) -> ClientResponse:
    """Persiste un client (colonnes ``nom``, ``prenom``, ``telephone``).

    Args:
        session: Session SQLAlchemy async.
        payload: Données client validées.

    Returns:
        ClientResponse: Client créé.

    Raises:
        N/A
    """
    client = Client(
        nom=payload.name,
        prenom=payload.first_name,
        telephone=payload.contact,
        adresse_expedition=payload.shipping_address,
    )
    session.add(client)
    await session.flush()
    await session.refresh(client)
    return ClientResponse(
        id=str(client.id),
        name=client.nom,
        first_name=client.prenom,
        contact=client.telephone,
        shipping_address=client.adresse_expedition,
    )
