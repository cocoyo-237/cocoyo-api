"""Exceptions métier et mapping vers codes HTTP."""

from fastapi import HTTPException, status


class DomainError(Exception):
    """Erreur métier de base pour la couche domaine/handlers.

    Contexte:
        Levée dans les handlers ; convertie en HTTP par les routers.

    Attributes:
        message: Message lisible pour l'API.
        status_code: Code HTTP suggéré.
    """

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        """Initialise une erreur domaine.

        Args:
            message: Détail de l'erreur.
            status_code: Code HTTP associé (défaut 400).

        Returns:
            None

        Effets de bord:
            N/A
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(DomainError):
    """Entité demandée introuvable (404)."""

    def __init__(self, message: str = "Ressource introuvable") -> None:
        """Crée une erreur 404.

        Args:
            message: Détail optionnel.

        Returns:
            None
        """
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(DomainError):
    """Authentification invalide ou absente (401)."""

    def __init__(self, message: str = "Non authentifié") -> None:
        """Crée une erreur 401.

        Args:
            message: Détail optionnel.

        Returns:
            None
        """
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ProductNotFoundError(NotFoundError):
    """Produit absent ou inactif."""

    def __init__(self, product_id: str) -> None:
        """Signale un produit introuvable.

        Args:
            product_id: Identifiant UUID du produit.

        Returns:
            None
        """
        super().__init__(f"Produit introuvable ou inactif : {product_id}")


class ClientNotFoundError(NotFoundError):
    """Client absent."""

    def __init__(self, client_id: str) -> None:
        """Signale un client introuvable.

        Args:
            client_id: Identifiant UUID du client.

        Returns:
            None
        """
        super().__init__(f"Client introuvable : {client_id}")


class OrderNotFoundError(NotFoundError):
    """Commande absente."""

    def __init__(self, order_id: str) -> None:
        """Signale une commande introuvable.

        Args:
            order_id: Identifiant UUID de la commande.

        Returns:
            None
        """
        super().__init__(f"Commande introuvable : {order_id}")


class InvalidOrderLineError(DomainError):
    """Ligne de commande invalide (taille, quantité, produit)."""

    def __init__(self, message: str) -> None:
        """Crée une erreur de validation de ligne.

        Args:
            message: Détail de l'invalidité.

        Returns:
            None
        """
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def domain_error_to_http(exc: DomainError) -> HTTPException:
    """Convertit une ``DomainError`` en ``HTTPException`` FastAPI.

    Contexte:
        Utilisé dans les routers pour uniformiser les réponses d'erreur.

    Args:
        exc: Exception métier levée par un handler.

    Returns:
        HTTPException: Exception prête pour ``raise`` dans une route.

    Effets de bord:
        N/A

    Exemple:
        >>> raise domain_error_to_http(NotFoundError("x"))
    """
    return HTTPException(status_code=exc.status_code, detail=exc.message)
