"""Routes HTTP - profil."""

from fastapi import APIRouter

from core.dependencies import CurrentUser
from features.auth.me.handler import handle_me
from features.auth.me.schemas import MeResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me", response_model=MeResponse, summary="Profil courant")
def me(current_user: CurrentUser) -> MeResponse:
    """Retourne l'utilisateur authentifié (JWT requis).

    HTTP:
        GET /auth/me - 200, 401.
    """
    return handle_me(current_user)
