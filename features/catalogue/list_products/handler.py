"""Handler liste articles."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from features.catalogue.create_product.handler import _article_to_response
from features.catalogue.list_products.schemas import ProductListResponse
from infrastructure.database.models.article import Article


async def handle_list_products(
    session: AsyncSession, active_only: bool = True, skip: int = 0, limit: int = 50
) -> ProductListResponse:
    """Liste ``articles`` ; ``active_only`` filtre ``quantite_stock > 0``.

    Args:
        session: Session async.
        active_only: Exclure stock zéro si true.
        skip: Offset.
        limit: Page size.

    Returns:
        ProductListResponse: Articles et total.

    Raises:
        N/A
    """
    query = select(Article)
    count_query = select(func.count()).select_from(Article)
    if active_only:
        query = query.where(Article.quantite_stock > 0)
        count_query = count_query.where(Article.quantite_stock > 0)

    total = (await session.execute(count_query)).scalar_one()
    result = await session.execute(query.order_by(Article.nom).offset(skip).limit(limit))
    articles = result.scalars().all()
    return ProductListResponse(
        items=[_article_to_response(a) for a in articles],
        total=total,
    )
