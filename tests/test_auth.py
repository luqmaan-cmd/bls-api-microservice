"""Tests for API key authentication middleware."""

from fastapi.testclient import TestClient


def test_no_key_required_when_no_keys_configured(client: TestClient, monkeypatch):
    """When API_KEYS env var is empty, requests should pass without a key."""
    # The conftest sets API_KEYS=test-key-123, so we need to monkeypatch
    # the settings object used by the middleware.
    from app.config import get_settings
    settings = get_settings()
    monkeypatch.setattr(settings, "api_keys", "")
    resp = client.get("/api/v1/cpi")
    # Will 200 with empty data (no key required)
    assert resp.status_code == 200


def test_missing_key_returns_401(client: TestClient):
    """When API_KEYS is set, omitting the key should return 401."""
    resp = client.get("/api/v1/cpi")
    assert resp.status_code == 401
    assert "API key required" in resp.json()["detail"]


def test_invalid_key_returns_401(client: TestClient):
    """An incorrect API key should return 401."""
    resp = client.get("/api/v1/cpi", headers={"X-API-Key": "wrong-key"})
    assert resp.status_code == 401
    assert "Invalid API key" in resp.json()["detail"]


def test_valid_key_header(client: TestClient):
    """A correct X-API-Key header should allow access."""
    resp = client.get("/api/v1/cpi", headers={"X-API-Key": "test-key-123"})
    assert resp.status_code == 200


def test_valid_key_query_param(client: TestClient):
    """A correct api_key query parameter should allow access."""
    resp = client.get("/api/v1/cpi?api_key=test-key-123")
    assert resp.status_code == 200


def test_root_and_health_exempt_from_auth(client: TestClient):
    """Root and health endpoints should not require an API key."""
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
