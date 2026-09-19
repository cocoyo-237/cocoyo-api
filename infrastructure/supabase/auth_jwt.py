"""Validation des JWT Supabase Auth."""

from core.exceptions import UnauthorizedError
from infrastructure.supabase.client import get_supabase_client


async def verify_access_token(token: str) -> dict:
    """Valide un access token JWT via l'API Supabase Auth.

    Contexte:
        ``core.dependencies.get_current_user``.

    Préconditions:
        Token non vide émis par Supabase pour ce projet.

    Comportement:
        1. Appelle ``auth.get_user(jwt)``.
        2. Vérifie la présence d'un utilisateur.
        3. Retourne un dict minimal ``id``, ``email``.

    Args:
        token: JWT brut (sans préfixe Bearer).

    Returns:
        dict: ``{"id": str, "email": str | None, "user": User}``.

    Raises:
        UnauthorizedError: Token invalide ou utilisateur absent.

    Effets de bord:
        Appel réseau vers Supabase.

    Exemple:
        >>> user = await verify_access_token("eyJ...")

    Voir aussi:
        ``get_supabase_client``.
    """
    client = get_supabase_client()
    try:
        response = client.auth.get_user(token)
    except Exception as exc:
        raise UnauthorizedError("Token invalide ou expiré") from exc

    if response.user is None:
        raise UnauthorizedError("Token invalide ou expiré")

    return {
        "id": response.user.id,
        "email": response.user.email,
        "user": response.user,
    }
