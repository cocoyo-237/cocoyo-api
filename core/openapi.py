"""Personnalisation du schéma OpenAPI pour Swagger UI / ReDoc."""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def configure_openapi(app: FastAPI) -> None:
    """Branche une génération OpenAPI enrichie (sécurité JWT, métadonnées).

    Contexte:
        Rend Swagger UI utilisable avec le bouton « Authorize » pour les routes protégées.

    Comportement:
        1. Génère le schéma via les routes FastAPI.
        2. Ajoute ``BearerAuth`` si absent (complément à ``HTTPBearer``).
        3. Mémorise le schéma sur l'application.

    Args:
        app: Instance FastAPI configurée avec les routers.

    Returns:
        None

    Effets de bord:
        Remplace ``app.openapi`` par une fonction personnalisée.

    Voir aussi:
        ``core.app_factory.create_app``, ``core.dependencies.http_bearer``.
    """

    def custom_openapi() -> dict:
        """Produit le schéma OpenAPI 3.x de l'API Cocoyo.

        Returns:
            dict: Schéma OpenAPI complet.
        """
        if app.openapi_schema is not None:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        components = schema.setdefault("components", {})
        security_schemes = components.setdefault("securitySchemes", {})
        security_schemes.setdefault(
            "HTTPBearer",
            {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": (
                    "Jeton d'accès Supabase. Obtenir via **POST /auth/login**, "
                    "puis saisir uniquement la valeur du token (sans le préfixe Bearer)."
                ),
            },
        )
        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi
