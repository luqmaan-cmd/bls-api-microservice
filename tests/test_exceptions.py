"""Tests for exception handlers and error responses."""

from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.exceptions import generic_exception_handler, ErrorResponse

HEADERS = {"X-API-Key": "test-key-123"}


class TestExceptionHandlers:
    """Verify that custom exception handlers return the expected error shape."""

    def test_validation_error_returns_422(self, client: TestClient):
        """An invalid query param type should trigger the validation handler."""
        # year_gte expects an int; passing a string should 422
        resp = client.get("/api/v1/ce?year_gte=notanumber", headers=HEADERS)
        assert resp.status_code == 422
        body = resp.json()
        assert "error" in body
        assert body["error"]["type"] == "validation_error"
        assert body["error"]["status_code"] == 422

    def test_generic_error_handler_format(self):
        """Verify the generic exception handler returns the correct JSON shape."""
        from fastapi import Request
        import asyncio

        # Create a minimal FastAPI app with the generic handler
        test_app = FastAPI()
        test_app.add_exception_handler(Exception, generic_exception_handler)

        @test_app.get("/fail")
        def fail_route():
            raise RuntimeError("boom")

        test_client = TestClient(test_app, raise_server_exceptions=False)
        resp = test_client.get("/fail")
        assert resp.status_code == 500
        body = resp.json()
        assert body["error"]["type"] == "internal_error"
        assert body["error"]["status_code"] == 500
