"""Configuration applicative chargée depuis les variables d'environnement."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Paramètres globaux de l'API Cocoyo.

    Contexte:
        Utilisé par ``core.app_factory`` et l'infrastructure Supabase/Postgres.

    Règles métier:
        N/A — valeurs techniques uniquement.

    Attributes:
        supabase_url: URL du projet Supabase.
        supabase_anon_key: Clé publique pour Auth côté serveur.
        supabase_service_role_key: Clé serveur (ne pas exposer).
        database_url: URL SQLAlchemy async vers Postgres Supabase.
        api_host: Hôte d'écoute Uvicorn.
        api_port: Port d'écoute Uvicorn.
        cors_origins: Origines CORS autorisées (séparées par des virgules).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    supabase_url: str = Field(
        default="https://placeholder.supabase.co",
        description="URL du projet Supabase (remplacer dans .env)",
    )
    supabase_anon_key: str = Field(
        default="placeholder-anon-key",
        description="Clé anon Supabase (remplacer dans .env)",
    )
    supabase_service_role_key: str = Field(
        default="",
        description="Clé service role (optionnelle si seule l'anon est utilisée pour Auth)",
    )
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
        description="URL async SQLAlchemy (remplacer dans .env)",
    )
    api_host: str = Field(default="0.0.0.0", description="Hôte HTTP")
    api_port: int = Field(default=8000, description="Port HTTP")
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Origines CORS séparées par des virgules",
    )


@lru_cache
def get_settings() -> Settings:
    """Retourne une instance singleton des paramètres applicatifs.

    Contexte:
        Injecté via ``Depends`` ou import direct dans l'infrastructure.

    Préconditions:
        Variables d'environnement ou fichier ``.env`` présents pour les champs requis.

    Comportement:
        1. Instancie ``Settings`` une seule fois (cache LRU).
        2. Retourne la même instance aux appels suivants.

    Returns:
        Settings: Configuration validée par Pydantic.

    Raises:
        ValidationError: Variable obligatoire manquante ou invalide.

    Effets de bord:
        N/A — lecture configuration uniquement.

    Exemple:
        >>> settings = get_settings()

    Voir aussi:
        ``core.app_factory.create_app``.
    """
    return Settings()
