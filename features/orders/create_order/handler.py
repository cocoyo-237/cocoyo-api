"""Handler création commande."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.exceptions import ClientNotFoundError, InvalidOrderLineError, ProductNotFoundError
from features.orders._shared import commande_to_response
from features.orders.create_order.schemas import CreateOrderRequest, OrderResponse
from infrastructure.database.models.article import Article
from infrastructure.database.models.client import Client
from infrastructure.database.models.commande import Commande
from infrastructure.database.models.ligne_commande import LigneCommande
from shared.enums import StatutLivraison, StatutPaiement


async def handle_create_order(
    session: AsyncSession, payload: CreateOrderRequest
) -> OrderResponse:
    """Crée ``commandes`` et ``lignes_commande`` avec prix figés.

    Args:
        session: Session SQLAlchemy async.

    Returns:
        Réponse du cas d''usage (DTO).

    Raises:
        Voir exceptions domaine propagées.
    """
    try:
        client_uuid = uuid.UUID(payload.client_id)
    except ValueError as exc:
        raise ClientNotFoundError(payload.client_id) from exc

    client_result = await session.execute(select(Client).where(Client.id == client_uuid))
    if client_result.scalar_one_or_none() is None:
        raise ClientNotFoundError(payload.client_id)

    product_ids = []
    for line in payload.lines:
        try:
            product_ids.append(uuid.UUID(line.product_id))
        except ValueError as exc:
            raise ProductNotFoundError(line.product_id) from exc

    articles_result = await session.execute(
        select(Article).where(
            Article.id.in_(product_ids),
            Article.quantite_stock > 0,
        )
    )
    articles = {a.id: a for a in articles_result.scalars().all()}

    lignes: list[LigneCommande] = []

    for req_line in payload.lines:
        aid = uuid.UUID(req_line.product_id)
        article = articles.get(aid)
        if article is None:
            raise ProductNotFoundError(req_line.product_id)

        colors = list(article.couleurs_disponibles or [])
        if req_line.size not in colors:
            raise InvalidOrderLineError(
                f"Couleur '{req_line.size}' invalide pour l'article {req_line.product_id}"
            )
        if (article.quantite_stock or 0) < req_line.quantity:
            raise InvalidOrderLineError("Stock insuffisant pour cet article")

        lignes.append(
            LigneCommande(
                article_id=aid,
                quantite=req_line.quantity,
                couleur_choisie=req_line.size,
                prix_unitaire_vente=Decimal(article.prix_vente),
                prix_unitaire_achat=Decimal(article.prix_achat),
            )
        )
        article.quantite_stock = (
            article.quantite_stock or 0) - req_line.quantity

    commande = Commande(
        client_id=client_uuid,
        statut_paiement=StatutPaiement.EN_ATTENTE,
        statut_livraison=StatutLivraison.NON_LIVRE,
        montant_avance=Decimal("0"),
        reduction=payload.reduction,
        lieu_livraison=payload.lieu_livraison,
        lignes=lignes,
    )
    session.add(commande)
    await session.flush()

    result = await session.execute(
        select(Commande)
        .where(Commande.id == commande.id)
        .options(selectinload(Commande.lignes))
    )
    loaded = result.scalar_one()
    return commande_to_response(loaded)
