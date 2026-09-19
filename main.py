"""Point d'entrée Uvicorn de l'API Cocoyo."""

from core.app_factory import create_app

app = create_app()


def run() -> None:
    """Lance le serveur Uvicorn avec la configuration environnement.

    Contexte:
        ``python -m main`` ou script console si défini.

    Comportement:
        Lit ``API_HOST`` et ``API_PORT`` via settings.

    Effets de bord:
        Processus serveur HTTP long running.

    Voir aussi:
        ``uvicorn main:app --reload``.
    """
    import uvicorn

    from core.config import get_settings

    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )


if __name__ == "__main__":
    run()
