"""Schémas — liste clients."""

from pydantic import BaseModel, Field

from features.clients.create_client.schemas import ClientResponse


class ClientListResponse(BaseModel):
    """Liste paginée simple de clients."""

    items: list[ClientResponse] = Field(default_factory=list, description="Clients")
    total: int = Field(..., description="Nombre total")
