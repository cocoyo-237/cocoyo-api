"""Modèle ORM table ``products``."""

import uuid
from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base, TimestampMixin


class Product(Base, TimestampMixin):
    """Vêtement du catalogue (Module PDF A).

    Attributes:
        sizes: Liste JSON des tailles disponibles (ex. ``["S","M","L"]``).
        unit_price: Prix unitaire courant (hors snapshot commande).
        is_active: Faux si produit désactivé (soft delete).
    """

    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    sizes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
