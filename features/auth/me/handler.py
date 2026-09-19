"""Handler profil courant."""

from features.auth.me.schemas import MeResponse


def handle_me(current_user: dict) -> MeResponse:
    """Construit la réponse profil à partir du JWT validé.

    Contexte:
        Auth — vérification de session.

    Préconditions:
        ``current_user`` fourni par ``get_current_user``.

    Args:
        current_user: Dict avec clés id/email.

    Returns:
        MeResponse: Profil minimal.

    Raises:
        N/A

    Effets de bord:
        N/A

    Exemple:
        >>> handle_me({"id": "uuid", "email": "a@b.com"})

    Voir aussi:
        ``core.dependencies.get_current_user``.
    """
    return MeResponse(id=current_user["id"], email=current_user.get("email"))
