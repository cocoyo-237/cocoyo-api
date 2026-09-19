"""Modèle ORM table ``commandes``."""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base, CreatedAtMixin
from shared.enums import StatutLivraison, StatutPaiement

if TYPE_CHECKING:
    from infrastructure.database.models.client import Client
    from infrastructure.database.models.ligne_commande import LigneCommande


class Commande(Base, CreatedAtMixin):
    """Commande client (table ``commandes``).

    Note:
        Pas de colonne ``total_amount`` - total calculé depuis ``lignes_commande``.
    """

    __tablename__ = "commandes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=True,
    )
    statut_paiement: Mapped[StatutPaiement | None] = mapped_column(
        SAEnum(
            StatutPaiement,
            name="statut_paiement_enum",
            native_enum=True,
            create_constraint=False,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=True,
        default=StatutPaiement.EN_ATTENTE,
    )
    montant_avance: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True, default=0
    )
    statut_livraison: Mapped[StatutLivraison | None] = mapped_column(
        SAEnum(
            StatutLivraison,
            name="statut_livraison_enum",
            native_enum=True,
            create_constraint=False,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=True,
        default=StatutLivraison.NON_LIVRE,
    )
    lieu_livraison: Mapped[str | None] = mapped_column(Text, nullable=True)
    reduction: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True, default=0)
    date_commande: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    gerant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True)

    client: Mapped["Client | None"] = relationship(back_populates="commandes")
    lignes: Mapped[list["LigneCommande"]] = relationship(
        back_populates="commande",
        cascade="all, delete-orphan",
    )
