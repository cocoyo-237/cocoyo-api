"""Dépendances FastAPI injectables (session DB, utilisateur courant)."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UnauthorizedError
from infrastructure.database.session import get_async_session
from infrastructure.supabase.auth_jwt import verify_access_token

DbSession = Annotated[AsyncSession, Depends(get_async_session)]

http_bearer = HTTPBearer(
    auto_error=False,
    description="JWT Supabase (POST /auth/login)",
)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(http_bearer)
    ] = None,
) -> dict:
    """Extrait et valide l'utilisateur Supabase depuis l'en-tête Authorization.

    Contexte:
        Protège les routes métier (catalogue, commandes, dashboard).

    Préconditions:
        En-tête ``Authorization: Bearer <access_token>`` présent et valide.

    Comportement:
        1. Vérifie le préfixe Bearer.
        2. Appelle Supabase pour valider le JWT.
        3. Retourne le payload utilisateur.

    Args:
        credentials: Jeton Bearer extrait par FastAPI (visible dans OpenAPI/Swagger).

    Returns:
        dict: Utilisateur Supabase (id, email, etc.).

    Raises:
        UnauthorizedError: Token absent, mal formé ou invalide.

    Effets de bord:
        Appel HTTP vers Supabase Auth (get_user).

    Exemple:
        >>> # Swagger : Authorize → coller le access_token de /auth/login

    Voir aussi:
        ``infrastructure.supabase.auth_jwt.verify_access_token``, ``core.openapi``.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError("Token d'accès manquant ou invalide")
    token = credentials.credentials.strip()
    if not token:
        raise UnauthorizedError("Token d'accès manquant ou invalide")
    return await verify_access_token(token)


CurrentUser = Annotated[dict, Depends(get_current_user)]


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Alias documenté pour la session async (générateur).

    Contexte:
        Permet une injection explicite dans les tests.

    Yields:
        AsyncSession: Session SQLAlchemy liée à la requête.

    Effets de bord:
        Commit/rollback gérés par ``get_async_session``.

    Voir aussi:
        ``infrastructure.database.session.get_async_session``.
    """
    async for session in get_async_session():
        yield session
