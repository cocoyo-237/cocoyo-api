"""Exemples de docstrings conformes pour le projet Cocoyo API.

Ce module sert de référence pour les développeurs ; il n'est pas importé
par l'application au runtime.
"""


async def handle_example_create_order(session, payload):
    """Crée une commande multi-articles avec calcul du total et snapshot des prix.

    Contexte:
        Module PDF B (prise de commande). Slice ``features/orders/create_order``.

    Préconditions:
        - Appelant authentifié (JWT Supabase valide).
        - ``client_id`` existe en base.
        - Chaque produit référencé est actif.

    Comportement:
        1. Charge les produits demandés.
        2. Valide quantités et tailles.
        3. Calcule le montant total.
        4. Persiste commande et lignes en une transaction.

    Règles métier:
        - Le prix unitaire des lignes est figé au moment de la commande.

    Transactions:
        Une transaction unique : insert ``orders`` + ``order_lines`` puis commit.

    Args:
        session: Session SQLAlchemy async.
        payload: Corps validé de la requête.

    Returns:
        Représentation de la commande créée.

    Raises:
        ProductNotFoundError: Produit absent ou inactif.

    Effets de bord:
        Écritures en base sur ``orders`` et ``order_lines``.

    Exemple:
        >>> # {"client_id": "...", "lines": [{"product_id": "...", "size": "M", "quantity": 2}]}

    Voir aussi:
        ``shared.order_totals.compute_order_total``.
    """
    raise NotImplementedError("Module de référence uniquement.")
