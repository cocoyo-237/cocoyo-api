"""Routes HTTP - connexion."""

from fastapi import APIRouter

from core.exceptions import DomainError, UnauthorizedError, domain_error_to_http
from features.auth.login.handler import handle_login
from features.auth.login.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse, summary="Connexion opérateur")
def login(payload: LoginRequest) -> LoginResponse:
    """Authentifie et retourne les jetons (public).

    HTTP:
        POST /auth/login - 200, 401, 422.
    """
    try:
        return handle_login(payload)
    except UnauthorizedError as exc:
        raise domain_error_to_http(exc) from exc
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
