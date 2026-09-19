"""Handler désactivation article (stock à zéro)."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ProductNotFoundError
from features.catalogue.create_product.handler import _article_to_response
from features.catalogue.create_product.schemas import ProductResponse
from infrastructure.database.models.article import Article


async def handle_deactivate_product(session: AsyncSession, product_id: str) -> ProductResponse:
    """Met ``quantite_stock`` à 0 (pas de colonne is_active en base).

    Args:
        session: Session SQLAlchemy async.

    Returns:
        Réponse du cas d''usage (DTO).

    Raises:
        Voir exceptions domaine propagées.
    """
    try:
        pid = uuid.UUID(product_id)
    except ValueError as exc:
        raise ProductNotFoundError(product_id) from exc

    result = await session.execute(select(Article).where(Article.id == pid))
    article = result.scalar_one_or_none()
    if article is None:
        raise ProductNotFoundError(product_id)

    article.quantite_stock = 0
    await session.flush()
    await session.refresh(article)
    return _article_to_response(article)
