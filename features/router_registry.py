"""Registre central des routers VSA pour montage dans FastAPI."""

from fastapi import APIRouter

from features.auth.login.router import router as login_router
from features.auth.me.router import router as me_router
from features.auth.register.router import router as register_router
from features.catalogue.create_product.router import router as create_product_router
from features.catalogue.deactivate_product.router import router as deactivate_product_router
from features.catalogue.list_products.router import router as list_products_router
from features.catalogue.update_product.router import router as update_product_router
from features.clients.create_client.router import router as create_client_router
from features.clients.list_clients.router import router as list_clients_router
from features.dashboard.get_overview.router import router as dashboard_overview_router
from features.orders.create_order.router import router as create_order_router
from features.orders.get_order.router import router as get_order_router
from features.orders.list_orders.router import router as list_orders_router
from features.orders.search_orders.router import router as search_orders_router
from features.orders.update_delivery_status.router import router as update_delivery_router
from features.orders.update_payment_status.router import router as update_payment_router


def get_api_routers() -> list[APIRouter]:
    """Retourne tous les routers métier dans un ordre compatible FastAPI.

    Contexte:
        ``/orders/search`` doit être enregistré avant ``/orders/{order_id}``.

    Returns:
        list[APIRouter]: Routers à inclure dans l'application.

    Effets de bord:
        N/A

    Voir aussi:
        ``core.app_factory.create_app``.
    """
    return [
        register_router,
        login_router,
        me_router,
        create_product_router,
        list_products_router,
        update_product_router,
        deactivate_product_router,
        create_client_router,
        list_clients_router,
        search_orders_router,
        list_orders_router,
        create_order_router,
        update_payment_router,
        update_delivery_router,
        get_order_router,
        dashboard_overview_router,
    ]
