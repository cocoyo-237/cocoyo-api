"""Factory de session SQLAlchemy async."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import get_settings

_engine = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine():
    """Retourne le moteur SQLAlchemy async (singleton lazy).

    Contexte:
        Infrastructure — connexion Postgres Supabase via pooler.

    Préconditions:
        ``DATABASE_URL`` défini dans l'environnement.

    Returns:
        AsyncEngine: Moteur asyncpg.

    Effets de bord:
        Crée le moteur au premier appel.

    Voir aussi:
        ``get_async_session``.
    """
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Retourne la factory de sessions async.

    Returns:
        async_sessionmaker: Factory configurée avec expire_on_commit=False.

    Effets de bord:
        Initialise le moteur si nécessaire.
    """
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Fournit une session DB par requête HTTP avec rollback en cas d'erreur.

    Contexte:
        Dépendance FastAPI via ``core.dependencies.DbSession``.

    Yields:
        AsyncSession: Session active.

    Comportement:
        1. Ouvre une session.
        2. Yield à l'endpoint/handler.
        3. Commit si pas d'exception, sinon rollback.

    Effets de bord:
        Commit ou rollback sur la base Postgres.

    Exemple:
        Utilisation via ``Depends(get_async_session)``.
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
