"""Modèles ORM alignés sur le schéma Supabase collaborateur."""

from infrastructure.database.models.article import Article
from infrastructure.database.models.client import Client
from infrastructure.database.models.commande import Commande
from infrastructure.database.models.ligne_commande import LigneCommande
from infrastructure.database.models.profile import Profile

# Alias rétrocompatibles (imports internes)
Product = Article
Order = Commande
OrderLine = LigneCommande

__all__ = [
    "Article",
    "Client",
    "Commande",
    "LigneCommande",
    "Profile",
    "Product",
    "Order",
    "OrderLine",
]
