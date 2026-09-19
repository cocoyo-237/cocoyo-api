"""Énumérations alignées sur les types Postgres du projet Supabase collaborateur."""

from enum import Enum


class StatutPaiement(str, Enum):
    """Type ``statut_paiement_enum`` en base."""

    EN_ATTENTE = "en_attente"
    AVANCE_PAYEE = "avance_payee"
    PAYE_INTEGRALEMENT = "paye_integralement"


class StatutLivraison(str, Enum):
    """Type ``statut_livraison_enum`` en base."""

    NON_LIVRE = "non_livre"
    EN_COURS = "en_cours"
    LIVRE = "livre"


# Alias API (anglais) → mêmes valeurs que ci-dessus pour OpenAPI
PaymentStatus = StatutPaiement
DeliveryStatus = StatutLivraison
