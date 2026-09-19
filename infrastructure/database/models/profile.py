"""Modèle ORM table ``profiles`` (profil gérant / boutique)."""

import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base, CreatedAtMixin


class Profile(Base, CreatedAtMixin):
    """Profil lié à ``auth.users`` (clé ``id`` = user id Supabase)."""

    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    nom_complet: Mapped[str | None] = mapped_column(String(150), nullable=True)
    nom_boutique: Mapped[str | None] = mapped_column(String(150), nullable=True)
    telephone: Mapped[str | None] = mapped_column(String(20), nullable=True)
