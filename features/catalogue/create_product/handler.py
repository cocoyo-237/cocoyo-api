"""Handler création produit."""

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DomainError
from features.catalogue.create_product.schemas import CreateProductRequest, ProductResponse
from infrastructure.database.models.product import Product


async def handle_create_product(
    session: AsyncSession, payload: CreateProductRequest
) -> ProductResponse:
    """Enregistre un vêtement dans le catalogue.

    Contexte:
        Module PDF A — création produit.

    Préconditions:
        JWT valide ; au moins une taille ; prix >= 0.

    Comportement:
        1. Valide tailles non vides.
        2. Insert produit ``is_active=True``.

    Args:
        session: Session async.
        payload: Données produit.

    Returns:
        ProductResponse: Produit créé.

    Raises:
        DomainError: Tailles invalides.

    Effets de bord:
        Insert ``products``.

    Exemple:
        >>> # {"name": "Robe", "category": "Robe", "sizes": ["S","M"], "unit_price": "10000"}

    Voir aussi:
        ``features.catalogue.deactivate_product``.
    """
    sizes = [s.strip() for s in payload.sizes if s.strip()]
    if not sizes:
        raise DomainError("Au moins une taille valide est requise")

    product = Product(
        name=payload.name,
        category=payload.category,
        sizes=sizes,
        unit_price=payload.unit_price,
        is_active=True,
    )
    session.add(product)
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
