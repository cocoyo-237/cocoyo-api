"""Routes — tableau de bord."""

from fastapi import APIRouter

from core.dependencies import CurrentUser, DbSession
from features.dashboard.get_overview.handler import handle_get_overview
from features.dashboard.get_overview.schemas import DashboardOverviewResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview", response_model=DashboardOverviewResponse, summary="Vue d'ensemble")
async def get_overview(
    session: DbSession,
    _user: CurrentUser,
) -> DashboardOverviewResponse:
    """Indicateurs dashboard (JWT). HTTP: 200, 401."""
    return await handle_get_overview(session)
