"""Modèle ORM table ``articles`` (catalogue - schéma Supabase collaborateur)."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base, CreatedAtMixin

if TYPE_CHECKING:
    from infrastructure.database.models.ligne_commande import LigneCommande


class Article(Base, CreatedAtMixin):
    """Article / vêtement du catalogue (table ``articles``).

    Attributes:
        couleurs_disponibles: Tableau Postgres ``text[]``.
        quantite_stock: Stock disponible (pas de colonne ``is_active``).
    """

    __tablename__ = "articles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    prix_vente: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    prix_achat: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantite_stock: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=0)
    couleurs_disponibles: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text), nullable=True
    )
    gerant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True)

    lignes: Mapped[list["LigneCommande"]] = relationship(
        back_populates="article")
