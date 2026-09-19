"""Modèle ORM table ``clients``."""

import uuid

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from infrastructure.database.models.order import Order


class Client(Base, TimestampMixin):
    """Client de la marque (acheteur via réseaux sociaux / direct).

    Contexte:
        Module PDF B — association client ↔ commandes.

    Attributes:
        id: UUID primaire.
        name: Nom affiché du client.
        contact: Téléphone, email ou handle réseau social.
        orders: Commandes liées (relation 1-N).
    """

    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact: Mapped[str] = mapped_column(Text, nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="client")
