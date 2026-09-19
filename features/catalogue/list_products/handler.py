"""Handler liste produits."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.catalogue.create_product.schemas import ProductResponse
from features.catalogue.list_products.schemas import ProductListResponse
from infrastructure.database.models.product import Product


async def handle_list_products(
    session: AsyncSession, active_only: bool = True, skip: int = 0, limit: int = 50
) -> ProductListResponse:
    """Liste le catalogue avec filtre actifs optionnel.

    Contexte:
        Module PDF A — consultation catalogue.

    Args:
        session: Session async.
        active_only: Si true, exclut produits désactivés.
        skip: Pagination offset.
        limit: Taille page.

    Returns:
        ProductListResponse: Produits et total.

    Raises:
        N/A

    Effets de bord:
        Lecture seule.

    Voir aussi:
        ``handle_deactivate_product``.
    """
    query = select(Product)
    count_query = select(func.count()).select_from(Product)
    if active_only:
        query = query.where(Product.is_active.is_(True))
        count_query = count_query.where(Product.is_active.is_(True))

    total = (await session.execute(count_query)).scalar_one()
    result = await session.execute(query.order_by(Product.name).offset(skip).limit(limit))
    products = result.scalars().all()
    items = [
        ProductResponse(
            id=str(p.id),
            name=p.name,
            category=p.category,
            sizes=list(p.sizes),
            unit_price=p.unit_price,
            is_active=p.is_active,
        )
        for p in products
    ]
    return ProductListResponse(items=items, total=total)
