"""Helpers partagés entre slices orders."""

from decimal import Decimal

from features.orders.schemas import OrderLineResponse, OrderResponse
from infrastructure.database.models.commande import Commande
from shared.order_totals import OrderLineInput, compute_order_total


def commande_total(commande: Commande) -> Decimal:
    """Calcule le total vente d'une commande (lignes − réduction)."""
    lines = [
        OrderLineInput(l.quantite or 0, l.prix_unitaire_vente)
        for l in commande.lignes
    ]
    reduction = commande.reduction or Decimal("0")
    return compute_order_total(lines, reduction=reduction)


def commande_to_response(commande: Commande) -> OrderResponse:
    """Mappe ``Commande`` ORM vers DTO API."""
    total = commande_total(commande)
    return OrderResponse(
        id=str(commande.id),
        client_id=str(commande.client_id) if commande.client_id else "",
        ordered_at=commande.date_commande or commande.created_at,
        payment_status=commande.statut_paiement,
        delivery_status=commande.statut_livraison,
        total_amount=total,
        deposit_amount=commande.montant_avance or Decimal("0"),
        reduction=commande.reduction or Decimal("0"),
        lieu_livraison=commande.lieu_livraison,
        lines=[
            OrderLineResponse(
                product_id=str(line.article_id) if line.article_id else "",
                size=line.couleur_choisie or "",
                quantity=line.quantite or 0,
                unit_price=line.prix_unitaire_vente,
                unit_cost=line.prix_unitaire_achat,
            )
            for line in commande.lignes
        ],
    )


order_to_response = commande_to_response
