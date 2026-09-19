"""Schémas — création client."""

from pydantic import BaseModel, Field


class CreateClientRequest(BaseModel):
    """Corps ``POST /clients`` (Module PDF B)."""

    name: str = Field(..., min_length=1, max_length=255, description="Nom du client")
    contact: str = Field(..., min_length=1, description="Téléphone, email ou handle")


class ClientResponse(BaseModel):
    """Représentation client API."""

    id: str = Field(..., description="UUID client")
    name: str = Field(..., description="Nom")
    contact: str = Field(..., description="Contact")
