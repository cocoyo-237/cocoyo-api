"""Modèle ORM table ``clients`` (schéma Supabase collaborateur)."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base, CreatedAtMixin

if TYPE_CHECKING:
    from infrastructure.database.models.commande import Commande


class Client(Base, CreatedAtMixin):
    """Client acheteur - colonnes ``nom``, ``prenom``, ``telephone``, etc.

    Contexte:
        Module PDF B - table ``clients`` sur le projet Supabase partagé.

    Attributes:
        gerant_id: Propriétaire (défaut ``auth.uid()`` côté Postgres).
    """

    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str | None] = mapped_column(String(100), nullable=True)
    telephone: Mapped[str] = mapped_column(String(20), nullable=False)
    adresse_expedition: Mapped[str | None] = mapped_column(Text, nullable=True)
    gerant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True)

    commandes: Mapped[list["Commande"]] = relationship(back_populates="client")
