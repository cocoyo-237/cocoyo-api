"""Routes — mise à jour produit."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from core.exceptions import DomainError, domain_error_to_http
from features.catalogue.create_product.schemas import ProductResponse
from features.catalogue.update_product.handler import handle_update_product
from features.catalogue.update_product.schemas import UpdateProductRequest

router = APIRouter(prefix="/catalogue/products", tags=["Catalogue"])


@router.patch("/{product_id}", response_model=ProductResponse, summary="Modifier un produit")
async def update_product(
    product_id: str,
    payload: UpdateProductRequest,
    session: DbSession,
    _user: CurrentUser,
) -> ProductResponse:
    """PATCH produit (JWT). HTTP: 200, 404, 422."""
    try:
        return await handle_update_product(session, product_id, payload)
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
