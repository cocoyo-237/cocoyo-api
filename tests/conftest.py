"""Configuration pytest — client FastAPI et variables d'environnement factices."""

from core.config import get_settings
import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://user:pass@localhost:5432/postgres",
)


get_settings.cache_clear()


@pytest.fixture
def client() -> TestClient:
    """Fournit un TestClient FastAPI pour tests smoke.

    Returns:
        TestClient: Client synchrone contre ``main.app``.

    Effets de bord:
        Importe l'application à la première utilisation.
    """
    from core.app_factory import create_app

    return TestClient(create_app())
