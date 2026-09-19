"""Factory de l'application FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from core.exception_handlers import register_exception_handlers
from core.openapi import configure_openapi
from features.router_registry import get_api_routers

OPENAPI_TAGS = [
    {"name": "Health", "description": "Santé de l'API"},
    {"name": "Auth", "description": "Inscription et connexion Supabase Auth"},
    {"name": "Catalogue", "description": "Module A - produits et tarifs"},
    {"name": "Clients", "description": "Clients pour les commandes"},
    {"name": "Orders", "description": "Modules B/C - commandes et statuts"},
    {"name": "Dashboard", "description": "Module D - indicateurs"},
]


def create_app() -> FastAPI:
    """Construit et configure l'application FastAPI Cocoyo.

    Contexte:
        Point d'entrée unique pour Uvicorn et les tests.

    Comportement:
        1. Instancie FastAPI avec métadonnées OpenAPI.
        2. Configure CORS depuis les settings.
        3. Enregistre les handlers d'erreurs métier.
        4. Monte tous les routers VSA.
        5. Expose ``GET /health``.

    Returns:
        FastAPI: Application prête à servir.

    Effets de bord:
        N/A

    Exemple:
        >>> app = create_app()

    Voir aussi:
        ``main.py``, ``features.router_registry``.
    """
    settings = get_settings()
    app = FastAPI(
        title="Cocoyo API",
        description=(
            "Back-office marque de vêtements - catalogue, commandes, dashboard.\n\n"
            "**Swagger :** utilisez `POST /auth/login`, puis **Authorize** avec le "
            "`access_token` (sans préfixe `Bearer`)."
        ),
        version="0.1.0",
        openapi_tags=OPENAPI_TAGS,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "filter": True,
        },
    )

    origins = [o.strip()
               for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    for router in get_api_routers():
        app.include_router(router)

    configure_openapi(app)

    @app.get("/health", tags=["Health"], summary="Santé de l'API")
    def health() -> dict[str, str]:
        """Vérifie que l'API répond (sans accès base).

        Returns:
            dict: Statut ok.

        HTTP:
            GET /health - 200.
        """
        return {"status": "ok"}

    return app
