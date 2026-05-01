"""Tests for root and health endpoints."""

from fastapi.testclient import TestClient


def test_root(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["message"] == "BLS Economic Data API"
    assert body["docs"] == "/docs"
    assert body["version"] == "1.0.0"


def test_health(client: TestClient):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
