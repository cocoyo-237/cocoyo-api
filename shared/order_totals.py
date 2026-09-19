"""Calculs financiers partagés pour les commandes."""

from decimal import Decimal
from typing import Sequence

from shared.enums import PaymentStatus


class OrderLineInput:
    """Structure minimale pour le calcul de total (quantity × unit_price).

    Attributes:
        quantity: Nombre d'unités (> 0).
        unit_price: Prix unitaire figé ou catalogue.
    """

    def __init__(self, quantity: int, unit_price: Decimal) -> None:
        """Construit une ligne de calcul.

        Args:
            quantity: Quantité strictement positive.
            unit_price: Prix unitaire non négatif.

        Raises:
            ValueError: Si quantity <= 0 ou prix négatif.
        """
        if quantity <= 0:
            raise ValueError("La quantité doit être strictement positive")
        if unit_price < 0:
            raise ValueError("Le prix unitaire ne peut pas être négatif")
        self.quantity = quantity
        self.unit_price = unit_price


def compute_order_total(lines: Sequence[OrderLineInput]) -> Decimal:
    """Calcule le montant total d'une commande à partir des lignes.

    Contexte:
        Module PDF B — utilisé à la création de commande.

    Préconditions:
        Au moins une ligne si appelé pour une commande non vide.

    Comportement:
        1. Pour chaque ligne, multiplie ``quantity`` par ``unit_price``.
        2. Somme les sous-totaux avec précision ``Decimal``.

    Règles métier:
        Pas de remise ni TVA dans cette version.

    Args:
        lines: Lignes avec quantité et prix unitaire.

    Returns:
        Decimal: Total arrondi à 2 décimales.

    Raises:
        ValueError: Ligne invalide via ``OrderLineInput``.

    Effets de bord:
        N/A

    Exemple:
        >>> compute_order_total([OrderLineInput(2, Decimal("25.00"))])
        Decimal('50.00')

    Voir aussi:
        ``features.orders.create_order.handler``.
    """
    total = Decimal("0")
    for line in lines:
        total += Decimal(line.quantity) * Decimal(line.unit_price)
    return total.quantize(Decimal("0.01"))


def compute_collected_revenue(
    total_amount: Decimal,
    payment_status: PaymentStatus,
    deposit_amount: Decimal,
) -> Decimal:
    """Détermine le montant encaissé pour une commande (dashboard CA).

    Contexte:
        Module PDF D — agrégat chiffre d'affaires encaissé.

    Règles métier:
        - ``PAID``: tout le ``total_amount``.
        - ``DEPOSIT``: ``deposit_amount`` uniquement.
        - ``UNPAID``: 0.

    Args:
        total_amount: Total de la commande.
        payment_status: Statut paiement courant.
        deposit_amount: Acompte enregistré si statut deposit.

    Returns:
        Decimal: Part encaissée pour cette commande.

    Effets de bord:
        N/A
    """
    if payment_status == PaymentStatus.PAID:
        return total_amount
    if payment_status == PaymentStatus.DEPOSIT:
        return deposit_amount
    return Decimal("0")


def compute_outstanding_amount(
    total_amount: Decimal,
    payment_status: PaymentStatus,
    deposit_amount: Decimal,
) -> Decimal:
    """Calcule le montant restant à recouvrer pour une commande.

    Contexte:
        Module PDF D — impayés.

    Règles métier:
        - ``UNPAID``: total intégral.
        - ``DEPOSIT``: ``total_amount - deposit_amount``.
        - ``PAID``: 0.

    Args:
        total_amount: Total commande.
        payment_status: Statut paiement.
        deposit_amount: Acompte déjà versé.

    Returns:
        Decimal: Reste à encaisser.

    Effets de bord:
        N/A
    """
    if payment_status == PaymentStatus.PAID:
        return Decimal("0")
    if payment_status == PaymentStatus.DEPOSIT:
        return (total_amount - deposit_amount).quantize(Decimal("0.01"))
    return total_amount
