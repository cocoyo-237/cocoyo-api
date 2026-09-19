"""Calculs financiers partagés pour les commandes."""

from decimal import Decimal
from typing import Sequence

from shared.enums import StatutPaiement


class OrderLineInput:
    """Structure minimale pour le calcul de total (quantity × unit_price)."""

    def __init__(self, quantity: int, unit_price: Decimal) -> None:
        """Construit une ligne de calcul."""
        if quantity <= 0:
            raise ValueError("La quantité doit être strictement positive")
        if unit_price < 0:
            raise ValueError("Le prix unitaire ne peut pas être négatif")
        self.quantity = quantity
        self.unit_price = unit_price


def compute_order_total(
    lines: Sequence[OrderLineInput], reduction: Decimal = Decimal("0")
) -> Decimal:
    """Calcule le montant total d'une commande (lignes − réduction)."""
    total = Decimal("0")
    for line in lines:
        total += Decimal(line.quantity) * Decimal(line.unit_price)
    total -= reduction
    if total < 0:
        total = Decimal("0")
    return total.quantize(Decimal("0.01"))


def compute_collected_revenue(
    total_amount: Decimal,
    payment_status: StatutPaiement | None,
    deposit_amount: Decimal | None,
) -> Decimal:
    """Montant encaissé selon ``statut_paiement`` et ``montant_avance``."""
    if payment_status == StatutPaiement.PAYE_INTEGRALEMENT:
        return total_amount
    if payment_status == StatutPaiement.AVANCE_PAYEE:
        return deposit_amount or Decimal("0")
    return Decimal("0")


def compute_outstanding_amount(
    total_amount: Decimal,
    payment_status: StatutPaiement | None,
    deposit_amount: Decimal | None,
) -> Decimal:
    """Reste à encaisser."""
    if payment_status == StatutPaiement.PAYE_INTEGRALEMENT:
        return Decimal("0")
    if payment_status == StatutPaiement.AVANCE_PAYEE:
        return (total_amount - (deposit_amount or Decimal("0"))).quantize(Decimal("0.01"))
    return total_amount
