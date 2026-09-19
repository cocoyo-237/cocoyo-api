"""Tests smoke API."""


def test_health_returns_ok(client) -> None:
    """Vérifie que GET /health renvoie 200 et status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
