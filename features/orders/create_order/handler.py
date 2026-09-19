"""Handler création commande."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import ClientNotFoundError, InvalidOrderLineError, ProductNotFoundError
from features.orders.create_order.schemas import (
    CreateOrderRequest,
    OrderLineResponse,
    OrderResponse,
)
from infrastructure.database.models.client import Client
from infrastructure.database.models.order import Order
from infrastructure.database.models.order_line import OrderLine
from infrastructure.database.models.product import Product
from shared.enums import DeliveryStatus, PaymentStatus
from shared.order_totals import OrderLineInput, compute_order_total


def _order_to_response(order: Order) -> OrderResponse:
    """Mappe un ORM Order vers OrderResponse.

    Args:
        order: Commande avec lignes chargées.

    Returns:
        OrderResponse: DTO API.
    """
    return OrderResponse(
        id=str(order.id),
        client_id=str(order.client_id),
        ordered_at=order.ordered_at,
        payment_status=order.payment_status,
        delivery_status=order.delivery_status,
        total_amount=order.total_amount,
        deposit_amount=order.deposit_amount,
        lines=[
            OrderLineResponse(
                product_id=str(line.product_id),
                size=line.size,
                quantity=line.quantity,
                unit_price=line.unit_price,
            )
            for line in order.lines
        ],
    )


async def handle_create_order(
    session: AsyncSession, payload: CreateOrderRequest
) -> OrderResponse:
    """Crée une commande multi-articles avec calcul du total et snapshot des prix.

    Contexte:
        Module PDF B — prise de commande panier.

    Préconditions:
        Client existant ; produits actifs ; tailles valides.

    Comportement:
        1. Vérifie le client.
        2. Charge les produits par id.
        3. Valide chaque ligne (taille, quantité).
        4. Calcule total via ``compute_order_total``.
        5. Insère order + order_lines.

    Transactions:
        Atomique via session unique (commit en fin de requête).

    Args:
        session: Session async.
        payload: Client et lignes panier.

    Returns:
        OrderResponse: Commande créée.

    Raises:
        ClientNotFoundError: Client absent.
        ProductNotFoundError: Produit absent/inactif.
        InvalidOrderLineError: Taille ou quantité invalide.

    Effets de bord:
        Insert ``orders`` et ``order_lines``.

    Exemple:
        >>> # {"client_id": "...", "lines": [{"product_id": "...", "size": "M", "quantity": 2}]}

    Voir aussi:
        ``shared.order_totals.compute_order_total``.
    """
    try:
        client_uuid = uuid.UUID(payload.client_id)
    except ValueError as exc:
        raise ClientNotFoundError(payload.client_id) from exc

    client_result = await session.execute(select(Client).where(Client.id == client_uuid))
    if client_result.scalar_one_or_none() is None:
        raise ClientNotFoundError(payload.client_id)

    product_ids = []
    for line in payload.lines:
        try:
            product_ids.append(uuid.UUID(line.product_id))
        except ValueError as exc:
            raise ProductNotFoundError(line.product_id) from exc

    products_result = await session.execute(
        select(Product).where(Product.id.in_(product_ids), Product.is_active.is_(True))
    )
    products = {p.id: p for p in products_result.scalars().all()}

    line_inputs: list[OrderLineInput] = []
    order_lines: list[OrderLine] = []

    for req_line in payload.lines:
        pid = uuid.UUID(req_line.product_id)
        product = products.get(pid)
        if product is None:
            raise ProductNotFoundError(req_line.product_id)

        sizes = list(product.sizes) if product.sizes else []
        if req_line.size not in sizes:
            raise InvalidOrderLineError(
                f"Taille '{req_line.size}' invalide pour le produit {req_line.product_id}"
            )

        unit_price = Decimal(product.unit_price)
        line_inputs.append(OrderLineInput(req_line.quantity, unit_price))
        order_lines.append(
            OrderLine(
                product_id=pid,
                size=req_line.size,
                quantity=req_line.quantity,
                unit_price=unit_price,
            )
        )

    total = compute_order_total(line_inputs)
    order = Order(
        client_id=client_uuid,
        payment_status=PaymentStatus.UNPAID,
        delivery_status=DeliveryStatus.NOT_DELIVERED,
        total_amount=total,
        deposit_amount=Decimal("0"),
        lines=order_lines,
    )
    session.add(order)
    await session.flush()

    result = await session.execute(
        select(Order)
        .where(Order.id == order.id)
        .options(selectinload(Order.lines))
    )
    loaded = result.scalar_one()
    return _order_to_response(loaded)
