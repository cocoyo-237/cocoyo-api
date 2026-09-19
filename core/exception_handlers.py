"""Handlers d'exceptions globaux FastAPI."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import DomainError


def register_exception_handlers(app: FastAPI) -> None:
    """Enregistre la conversion des erreurs métier en JSON HTTP.

    Args:
        app: Instance FastAPI.

    Returns:
        None

    Effets de bord:
        Modifie les handlers d'exception de l'app.
    """

    @app.exception_handler(DomainError)
    async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
        """Transforme ``DomainError`` en réponse JSON.

        Args:
            _request: Requête HTTP.
            exc: Erreur métier.

        Returns:
            JSONResponse: Corps ``detail`` et statut HTTP.
        """
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
