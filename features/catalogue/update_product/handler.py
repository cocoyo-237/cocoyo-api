"""Handler mise à jour produit."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DomainError, ProductNotFoundError
from features.catalogue.create_product.schemas import ProductResponse
from features.catalogue.update_product.schemas import UpdateProductRequest
from infrastructure.database.models.product import Product


async def handle_update_product(
    session: AsyncSession, product_id: str, payload: UpdateProductRequest
) -> ProductResponse:
    """Met à jour partiellement un produit existant.

    Contexte:
        Module PDF A — modification catalogue.

    Préconditions:
        Produit existant (actif ou non).

    Args:
        session: Session async.
        product_id: UUID produit.
        payload: Champs optionnels à modifier.

    Returns:
        ProductResponse: Produit après mise à jour.

    Raises:
        ProductNotFoundError: ID inconnu.
        DomainError: Tailles vides si fournies.

    Effets de bord:
        Update ``products``.

    Voir aussi:
        ``handle_list_products``.
    """
    try:
        pid = uuid.UUID(product_id)
    except ValueError as exc:
        raise ProductNotFoundError(product_id) from exc

    result = await session.execute(select(Product).where(Product.id == pid))
    product = result.scalar_one_or_none()
    if product is None:
        raise ProductNotFoundError(product_id)

    if payload.name is not None:
        product.name = payload.name
    if payload.category is not None:
        product.category = payload.category
    if payload.sizes is not None:
        sizes = [s.strip() for s in payload.sizes if s.strip()]
        if not sizes:
            raise DomainError("Au moins une taille valide est requise")
        product.sizes = sizes
    if payload.unit_price is not None:
        product.unit_price = payload.unit_price

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
