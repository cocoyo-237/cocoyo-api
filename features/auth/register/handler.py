"""Handler inscription Supabase."""

from core.exceptions import DomainError
from features.auth.register.schemas import RegisterRequest, RegisterResponse
from infrastructure.supabase.client import get_supabase_client


def handle_register(payload: RegisterRequest) -> RegisterResponse:
    """Inscrit un nouvel utilisateur back-office via Supabase Auth.

    Contexte:
        Auth — hors modules PDF A-D, prérequis sécurité API.

    Préconditions:
        Email non déjà utilisé côté Supabase (sinon erreur Auth).

    Comportement:
        1. Appelle ``sign_up`` avec email/mot de passe.
        2. Retourne l'identifiant utilisateur créé.

    Règles métier:
        N/A — délégué à Supabase (confirmation email selon config projet).

    Transactions:
        N/A — pas d'écriture Postgres métier.

    Args:
        payload: Email et mot de passe validés.

    Returns:
        RegisterResponse: Identifiant et email.

    Raises:
        DomainError: Échec Supabase (email invalide, doublon, etc.).

    Effets de bord:
        Création utilisateur dans Supabase Auth.

    Exemple:
        >>> handle_register(RegisterRequest(email="a@b.com", password="longpass12"))

    Voir aussi:
        ``features.auth.login.handler``.
    """
    client = get_supabase_client()
    try:
        result = client.auth.sign_up({"email": payload.email, "password": payload.password})
    except Exception as exc:
        raise DomainError(f"Inscription impossible : {exc}") from exc

    if result.user is None:
        raise DomainError("Inscription impossible : utilisateur non créé")

    return RegisterResponse(
        user_id=result.user.id,
        email=payload.email,
    )
