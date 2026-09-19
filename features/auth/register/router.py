"""Routes HTTP — inscription."""

from fastapi import APIRouter

from core.exceptions import DomainError, domain_error_to_http
from features.auth.register.handler import handle_register
from features.auth.register.schemas import RegisterRequest, RegisterResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
    summary="Inscription opérateur",
)
def register(payload: RegisterRequest) -> RegisterResponse:
    """Inscrit un compte back-office (public).

    HTTP:
        POST /auth/register — 201, 400, 422.

    Voir aussi:
        ``handle_register``.
    """
    try:
        return handle_register(payload)
    except DomainError as exc:
        raise domain_error_to_http(exc) from exc
