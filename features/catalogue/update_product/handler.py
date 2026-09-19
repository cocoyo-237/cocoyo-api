"""Handler mise à jour article."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DomainError, ProductNotFoundError
from features.catalogue.create_product.handler import _article_to_response
from features.catalogue.create_product.schemas import ProductResponse
from features.catalogue.update_product.schemas import UpdateProductRequest
from infrastructure.database.models.article import Article


async def handle_update_product(
    session: AsyncSession, product_id: str, payload: UpdateProductRequest
) -> ProductResponse:
    """Met à jour partiellement un ``articles``.

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

    if payload.name is not None:
        article.nom = payload.name
    if payload.sale_price is not None:
        article.prix_vente = payload.sale_price
    if payload.purchase_price is not None:
        article.prix_achat = payload.purchase_price
    if payload.colors is not None:
        colors = [c.strip() for c in payload.colors if c.strip()]
        if not colors:
            raise DomainError("Au moins une couleur valide est requise")
        article.couleurs_disponibles = colors
    if payload.image_url is not None:
        article.image_url = payload.image_url
    if payload.stock_quantity is not None:
        article.quantite_stock = payload.stock_quantity

    await session.flush()
    await session.refresh(article)
    return _article_to_response(article)
