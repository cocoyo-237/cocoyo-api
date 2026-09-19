"""Modèle ORM table ``orders``."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base, TimestampMixin
from shared.enums import DeliveryStatus, PaymentStatus


class Order(Base, TimestampMixin):
    """Commande client avec statuts paiement et livraison (Modules PDF B/C).

    Attributes:
        total_amount: Montant total calculé à la création.
        deposit_amount: Montant déjà encaissé si statut ``deposit``.
    """

    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False
    )
    ordered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SAEnum(
            PaymentStatus,
            name="payment_status",
            native_enum=True,
            create_constraint=False,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
        default=PaymentStatus.UNPAID,
    )
    delivery_status: Mapped[DeliveryStatus] = mapped_column(
        SAEnum(
            DeliveryStatus,
            name="delivery_status",
            native_enum=True,
            create_constraint=False,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
        default=DeliveryStatus.NOT_DELIVERED,
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    deposit_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    client: Mapped["Client"] = relationship(back_populates="orders")
    lines: Mapped[list["OrderLine"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


from infrastructure.database.models.client import Client  # noqa: E402
from infrastructure.database.models.order_line import OrderLine  # noqa: E402
