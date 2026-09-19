"""Schémas - création client."""

from pydantic import BaseModel, Field


class CreateClientRequest(BaseModel):
    """Corps ``POST /clients`` - mappé sur table ``clients``."""

    name: str = Field(..., min_length=1, max_length=100,
                      description="Nom de famille (colonne nom)")
    first_name: str | None = Field(
        default=None, max_length=100, description="Prénom")
    contact: str = Field(..., min_length=1, max_length=20,
                         description="Téléphone")
    shipping_address: str | None = Field(
        default=None, description="Adresse d'expédition")


class ClientResponse(BaseModel):
    """Représentation client API."""

    id: str = Field(..., description="UUID client")
    name: str = Field(..., description="Nom")
    first_name: str | None = Field(default=None, description="Prénom")
    contact: str = Field(..., description="Téléphone")
    shipping_address: str | None = Field(
        default=None, description="Adresse expédition")
