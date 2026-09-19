"""Routes — création produit."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from core.exceptions import DomainError, domain_error_to_http
from features.catalogue.create_product.handler import handle_create_product
from features.catalogue.create_product.schemas import CreateProductRequest, ProductResponse

router = APIRouter(prefix="/catalogue/products", tags=["Catalogue"])


@router.post("", response_model=ProductResponse, status_code=201, summary="Créer un produit")
async def create_product(
    payload: CreateProductRequest,
    session: DbSession,
    _user: CurrentUser,
) -> ProductResponse:
    """Crée un produit catalogue (JWT). HTTP: 201, 400, 401, 422."""
    try:
        return await handle_create_product(session, payload)
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
