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


class TimestampMixin:
    """Colonnes ``created_at`` et ``updated_at`` automatiques.

    Règles métier:
        ``updated_at`` est rafraîchi côté application à chaque mise à jour.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
