"""Client Supabase singleton pour l'authentification."""

from functools import lru_cache

from supabase import Client, create_client

from core.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    """Retourne le client Supabase configuré avec la clé anon.

    Contexte:
        Auth register/login — pas d'exposition de la service_role aux routes.

    Préconditions:
        ``SUPABASE_URL`` et ``SUPABASE_ANON_KEY`` définis.

    Returns:
        Client: Instance supabase-py.

    Effets de bord:
        N/A — connexion lazy.

    Voir aussi:
        ``infrastructure.supabase.auth_jwt``.
    """
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)
