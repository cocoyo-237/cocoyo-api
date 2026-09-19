"""Énumérations métier alignées sur le schéma PostgreSQL Supabase."""

from enum import Enum


class PaymentStatus(str, Enum):
    """Statut de paiement d'une commande (Module PDF C).

    Valeurs:
        UNPAID: Non payé.
        DEPOSIT: Acompte versé (montant partiel dans ``deposit_amount``).
        PAID: Intégralement payé.
    """

    UNPAID = "unpaid"
    DEPOSIT = "deposit"
    PAID = "paid"


class DeliveryStatus(str, Enum):
    """Statut de livraison d'une commande (Module PDF C).

    Valeurs:
        NOT_DELIVERED: Non livré.
        SHIPPING: En cours d'expédition.
        DELIVERED: Livré.
    """

    NOT_DELIVERED = "not_delivered"
    SHIPPING = "shipping"
    DELIVERED = "delivered"
