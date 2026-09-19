"""Handler connexion Supabase."""

from core.exceptions import DomainError, UnauthorizedError
from features.auth.login.schemas import LoginRequest, LoginResponse
from infrastructure.supabase.client import get_supabase_client


def handle_login(payload: LoginRequest) -> LoginResponse:
    """Authentifie un opérateur et retourne les jetons Supabase.

    Contexte:
        Auth - accès aux routes protégées.

    Préconditions:
        Compte existant et mot de passe correct.

    Comportement:
        1. ``sign_in_with_password``.
        2. Extrait access/refresh tokens de la session.

    Transactions:
        N/A

    Args:
        payload: Identifiants.

    Returns:
        LoginResponse: Jetons OAuth2.

    Raises:
        UnauthorizedError: Identifiants incorrects.
        DomainError: Erreur technique Supabase.

    Effets de bord:
        Session Supabase créée.

    Exemple:
        >>> handle_login(LoginRequest(email="a@b.com", password="secret"))

    Voir aussi:
        ``core.dependencies.get_current_user``.
    """
    client = get_supabase_client()
    try:
        result = client.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as exc:
        raise UnauthorizedError("Email ou mot de passe incorrect") from exc

    if result.session is None:
        raise UnauthorizedError("Email ou mot de passe incorrect")

    return LoginResponse(
        access_token=result.session.access_token,
        refresh_token=result.session.refresh_token,
        expires_in=result.session.expires_in,
    )
