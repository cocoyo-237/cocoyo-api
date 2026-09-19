"""Modèle ORM table ``lignes_commande``."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.article import Article
    from infrastructure.database.models.commande import Commande


class LigneCommande(Base):
    """Ligne de panier avec prix vente/achat figés."""

    __tablename__ = "lignes_commande"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    commande_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("commandes.id", ondelete="CASCADE"),
        nullable=True,
    )
    article_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("articles.id", ondelete="RESTRICT"),
        nullable=True,
    )
    quantite: Mapped[int | None] = mapped_column(Integer, nullable=True, default=1)
    couleur_choisie: Mapped[str | None] = mapped_column(String(50), nullable=True)
    prix_unitaire_vente: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    prix_unitaire_achat: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    commande: Mapped["Commande | None"] = relationship(back_populates="lignes")
    article: Mapped["Article | None"] = relationship(back_populates="lignes")
