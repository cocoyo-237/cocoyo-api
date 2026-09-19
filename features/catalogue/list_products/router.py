"""Routes — liste produits."""

from fastapi import APIRouter, Query

from core.dependencies import CurrentUser, DbSession
from features.catalogue.list_products.handler import handle_list_products
from features.catalogue.list_products.schemas import ProductListResponse

router = APIRouter(prefix="/catalogue/products", tags=["Catalogue"])


@router.get("", response_model=ProductListResponse, summary="Lister les produits")
async def list_products(
    session: DbSession,
    _user: CurrentUser,
    active_only: bool = Query(True, description="Uniquement produits actifs"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> ProductListResponse:
    """Liste le catalogue (JWT). HTTP: 200, 401."""
    return await handle_list_products(session, active_only=active_only, skip=skip, limit=limit)
