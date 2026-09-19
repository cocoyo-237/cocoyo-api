"""Tests OpenAPI / Swagger UI."""

import json


def test_openapi_json_available(client) -> None:
    """GET /openapi.json doit renvoyer un schéma OpenAPI 3 valide."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["openapi"].startswith("3.")
    assert schema["info"]["title"] == "Cocoyo API"
    assert "/health" in schema["paths"]
    assert "/auth/login" in schema["paths"]
    assert len(schema["paths"]) >= 14


def test_swagger_ui_available(client) -> None:
    """GET /docs doit servir Swagger UI (HTML)."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_redoc_available(client) -> None:
    """GET /redoc doit servir ReDoc."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower()


def test_protected_route_declares_bearer_security(client) -> None:
    """Les routes protégées doivent exiger HTTPBearer dans OpenAPI."""
    schema = client.get("/openapi.json").json()
    me_op = schema["paths"]["/auth/me"]["get"]
    assert "security" in me_op
    assert {"HTTPBearer": []} in me_op["security"]

    login_op = schema["paths"]["/auth/login"]["post"]
    assert "security" not in login_op or login_op.get("security") in (None, [])


def test_openapi_schema_is_json_serializable(client) -> None:
    """Le schéma complet doit être sérialisable (pas d'objet non-JSON)."""
    schema = client.get("/openapi.json").json()
    json.dumps(schema)
