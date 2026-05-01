"""Tests for pagination, range filters, and comma-separated OR filters."""

from fastapi.testclient import TestClient

from tests.conftest import seed_ce

HEADERS = {"X-API-Key": "test-key-123"}


class TestPagination:
    """Test limit, offset, page, has_more, and total."""

    def test_default_limit(self, client: TestClient, db_session):
        for i in range(5):
            seed_ce(db_session, series_id=f"CEU{i:012d}", year=2020 + i)
        resp = client.get("/api/v1/ce", headers=HEADERS)
        body = resp.json()
        assert body["limit"] == 100
        assert body["offset"] == 0
        assert body["total"] == 5
        assert body["has_more"] is False
        assert len(body["data"]) == 5

    def test_custom_limit(self, client: TestClient, db_session):
        for i in range(5):
            seed_ce(db_session, series_id=f"CEU{i:012d}", year=2020 + i)
        resp = client.get("/api/v1/ce?limit=2", headers=HEADERS)
        body = resp.json()
        assert body["limit"] == 2
        assert len(body["data"]) == 2
        assert body["has_more"] is True
        assert body["total"] == 5

    def test_offset(self, client: TestClient, db_session):
        for i in range(5):
            seed_ce(db_session, series_id=f"CEU{i:012d}", year=2020 + i)
        resp = client.get("/api/v1/ce?limit=2&offset=2", headers=HEADERS)
        body = resp.json()
        assert body["offset"] == 2
        assert len(body["data"]) == 2
        assert body["has_more"] is True

    def test_page_parameter(self, client: TestClient, db_session):
        for i in range(5):
            seed_ce(db_session, series_id=f"CEU{i:012d}", year=2020 + i)
        resp = client.get("/api/v1/ce?limit=2&page=2", headers=HEADERS)
        body = resp.json()
        # page=2 with limit=2 → offset=2
        assert body["offset"] == 2
        assert len(body["data"]) == 2

    def test_has_more_false_at_end(self, client: TestClient, db_session):
        for i in range(3):
            seed_ce(db_session, series_id=f"CEU{i:012d}", year=2020 + i)
        resp = client.get("/api/v1/ce?limit=10", headers=HEADERS)
        body = resp.json()
        assert body["has_more"] is False

    def test_empty_result(self, client: TestClient, db_session):
        resp = client.get("/api/v1/ce", headers=HEADERS)
        body = resp.json()
        assert body["data"] == []
        assert body["total"] == 0
        assert body["has_more"] is False

    def test_offset_beyond_results(self, client: TestClient, db_session):
        seed_ce(db_session)
        resp = client.get("/api/v1/ce?offset=100", headers=HEADERS)
        body = resp.json()
        assert body["data"] == []
        assert body["total"] == 1
        assert body["has_more"] is False


class TestRangeFilters:
    """Test year_gte, year_lte, year_gt, year_lt."""

    def test_year_gte(self, client: TestClient, db_session):
        seed_ce(db_session, year=2020)
        seed_ce(db_session, series_id="CEU0000000002", year=2023)
        resp = client.get("/api/v1/ce?year_gte=2022", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["year"] == 2023

    def test_year_lte(self, client: TestClient, db_session):
        seed_ce(db_session, year=2020)
        seed_ce(db_session, series_id="CEU0000000002", year=2023)
        resp = client.get("/api/v1/ce?year_lte=2021", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["year"] == 2020

    def test_year_gt(self, client: TestClient, db_session):
        seed_ce(db_session, year=2020)
        seed_ce(db_session, series_id="CEU0000000002", year=2023)
        resp = client.get("/api/v1/ce?year_gt=2020", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["year"] == 2023

    def test_year_lt(self, client: TestClient, db_session):
        seed_ce(db_session, year=2020)
        seed_ce(db_session, series_id="CEU0000000002", year=2023)
        resp = client.get("/api/v1/ce?year_lt=2023", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["year"] == 2020

    def test_year_range_combined(self, client: TestClient, db_session):
        for y in [2019, 2020, 2021, 2022, 2023]:
            seed_ce(db_session, series_id=f"CEU{y}00000000", year=y)
        resp = client.get("/api/v1/ce?year_gte=2020&year_lte=2022", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 3
        years = {d["year"] for d in body["data"]}
        assert years == {2020, 2021, 2022}


class TestCommaSeparatedFilters:
    """Test comma-separated OR filters for year and series_id."""

    def test_multi_year(self, client: TestClient, db_session):
        seed_ce(db_session, year=2020)
        seed_ce(db_session, series_id="CEU0000000002", year=2021)
        seed_ce(db_session, series_id="CEU0000000003", year=2022)
        resp = client.get("/api/v1/ce?year=2020,2022", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 2
        years = {d["year"] for d in body["data"]}
        assert years == {2020, 2022}

    def test_multi_series_id(self, client: TestClient, db_session):
        seed_ce(db_session, series_id="CEU0000000001")
        seed_ce(db_session, series_id="CEU0000000002")
        seed_ce(db_session, series_id="CEU0000000003")
        resp = client.get("/api/v1/ce?series_id=CEU0000000001,CEU0000000003", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 2

    def test_multi_value_dataset_filter(self, client: TestClient, db_session):
        """Comma-separated values on a dataset-specific filter (e.g. seasonal_code)."""
        seed_ce(db_session, seasonal_code="S")
        seed_ce(db_session, series_id="CEU0000000002", seasonal_code="U")
        resp = client.get("/api/v1/ce?seasonal_code=S,U", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 2
