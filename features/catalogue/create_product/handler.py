"""Handler création article."""

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DomainError
from features.catalogue.create_product.schemas import CreateProductRequest, ProductResponse
from infrastructure.database.models.article import Article


def _article_to_response(article: Article) -> ProductResponse:
    """Mappe ORM Article vers DTO."""
    stock = article.quantite_stock or 0
    return ProductResponse(
        id=str(article.id),
        name=article.nom,
        sale_price=article.prix_vente,
        purchase_price=article.prix_achat,
        colors=list(article.couleurs_disponibles or []),
        image_url=article.image_url,
        stock_quantity=stock,
        is_active=stock > 0,
    )


async def handle_create_product(
    session: AsyncSession, payload: CreateProductRequest
) -> ProductResponse:
    """Insère un enregistrement dans ``articles``.

    Args:
        session: Session async SQLAlchemy.
        payload: Données article validées.

    Returns:
        ProductResponse: Article créé.

    Raises:
        DomainError: Couleurs vides.
    """
    colors = [c.strip() for c in payload.colors if c.strip()]
    if not colors:
        raise DomainError("Au moins une couleur disponible est requise")

    article = Article(
        nom=payload.name,
        prix_vente=payload.sale_price,
        prix_achat=payload.purchase_price,
        couleurs_disponibles=colors,
        image_url=payload.image_url,
        quantite_stock=payload.stock_quantity,
    )
    session.add(article)
    await session.flush()
    await session.refresh(article)
    return _article_to_response(article)
