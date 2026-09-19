"""Base déclarative SQLAlchemy et mixins communs."""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Classe de base pour tous les modèles ORM Cocoyo.

    Contexte:
        Centralise le metadata SQLAlchemy pour les migrations et requêtes.

    Effets de bord:
        N/A
    """


class CreatedAtMixin:
    """Colonne ``created_at`` alignée sur le schéma Supabase collaborateur."""

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
