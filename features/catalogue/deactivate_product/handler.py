"""Handler désactivation produit."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ProductNotFoundError
from features.catalogue.create_product.schemas import ProductResponse
from infrastructure.database.models.product import Product


async def handle_deactivate_product(session: AsyncSession, product_id: str) -> ProductResponse:
    """Désactive un produit (soft delete).

    Contexte:
        Module PDF A — retrait du catalogue actif sans supprimer l'historique.

    Args:
        session: Session async.
        product_id: UUID produit.

    Returns:
        ProductResponse: Produit avec ``is_active=False``.

    Raises:
        ProductNotFoundError: Produit inconnu.

    Effets de bord:
        Update ``is_active``.

    Voir aussi:
        ``handle_list_products`` avec ``active_only=True``.
    """
    try:
        pid = uuid.UUID(product_id)
    except ValueError as exc:
        raise ProductNotFoundError(product_id) from exc

    result = await session.execute(select(Product).where(Product.id == pid))
    product = result.scalar_one_or_none()
    if product is None:
        raise ProductNotFoundError(product_id)

    product.is_active = False
    await session.flush()
    await session.refresh(product)
    return ProductResponse(
        id=str(product.id),
        name=product.name,
        category=product.category,
        sizes=list(product.sizes),
        unit_price=product.unit_price,
        is_active=product.is_active,
    )
