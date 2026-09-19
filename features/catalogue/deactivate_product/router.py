"""Routes — désactivation produit."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from features.catalogue.create_product.schemas import ProductResponse
from features.catalogue.deactivate_product.handler import handle_deactivate_product

router = APIRouter(prefix="/catalogue/products", tags=["Catalogue"])


@router.post(
    "/{product_id}/deactivate",
    response_model=ProductResponse,
    summary="Désactiver un produit",
)
async def deactivate_product(
    product_id: str,
    session: DbSession,
    _user: CurrentUser,
) -> ProductResponse:
    """Soft delete produit (JWT). HTTP: 200, 404."""
    return await handle_deactivate_product(session, product_id)
