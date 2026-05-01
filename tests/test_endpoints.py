"""Tests for all 10 dataset endpoints: basic retrieval, filtering, pagination."""

from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import (
    seed_ce, seed_cpi, seed_ppi, seed_jt, seed_la,
    seed_ci, seed_mp, seed_oe, seed_sa, seed_sm,
)

HEADERS = {"X-API-Key": "test-key-123"}


# ── CE ──────────────────────────────────────────────────────────────────────

class TestCEEndpoint:
    def test_empty(self, client: TestClient):
        resp = client.get("/api/v1/ce", headers=HEADERS)
        assert resp.status_code == 200
        body = resp.json()
        assert body["data"] == []
        assert body["total"] == 0

    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_ce(db_session)
        resp = client.get("/api/v1/ce", headers=HEADERS)
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["data"]) == 1
        assert body["total"] == 1
        assert body["data"][0]["series_id"] == "CEU0000000001"

    def test_filter_by_year(self, client: TestClient, db_session):
        seed_ce(db_session, year=2022)
        seed_ce(db_session, series_id="CEU0000000002", year=2023)
        resp = client.get("/api/v1/ce?year=2023", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["year"] == 2023

    def test_filter_by_industry_code(self, client: TestClient, db_session):
        seed_ce(db_session, industry_code="100000")
        seed_ce(db_session, series_id="CEU0000000002", industry_code="200000")
        resp = client.get("/api/v1/ce?industry_code=100000", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["industry_code"] == "100000"

    def test_period_name_in_response(self, client: TestClient, db_session):
        seed_ce(db_session)
        resp = client.get("/api/v1/ce", headers=HEADERS)
        assert resp.json()["data"][0]["period_name"] == "January"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_ce(db_session, period="01")
        seed_ce(db_session, series_id="CEU0000000002", period="02")
        resp = client.get("/api/v1/ce?period=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "02"


# ── CPI ─────────────────────────────────────────────────────────────────────

class TestCPIEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_cpi(db_session)
        resp = client.get("/api/v1/cpi", headers=HEADERS)
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["series_id"] == "CUSR0000SA0"

    def test_filter_by_area_code(self, client: TestClient, db_session):
        seed_cpi(db_session, area_code="0000")
        seed_cpi(db_session, series_id="CUSR0100SA0", area_code="0100")
        resp = client.get("/api/v1/cpi?area_code=0100", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["area_code"] == "0100"

    def test_filter_by_item_code(self, client: TestClient, db_session):
        seed_cpi(db_session, item_code="SA0")
        resp = client.get("/api/v1/cpi?item_code=SA0", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_seasonal_code(self, client: TestClient, db_session):
        seed_cpi(db_session, seasonal_code="S")
        seed_cpi(db_session, series_id="CUSR0000SA0U", seasonal_code="U")
        resp = client.get("/api/v1/cpi?seasonal_code=U", headers=HEADERS)
        assert resp.json()["total"] == 1
        assert resp.json()["data"][0]["seasonal_code"] == "U"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_cpi(db_session, period="M01")
        seed_cpi(db_session, series_id="CUSR0000SA0M02", period="M02")
        resp = client.get("/api/v1/cpi?period=M02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "M02"


# ── PPI ─────────────────────────────────────────────────────────────────────

class TestPPIEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_ppi(db_session)
        resp = client.get("/api/v1/ppi", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_filter_by_sector_code(self, client: TestClient, db_session):
        seed_ppi(db_session, sector_code="10")
        seed_ppi(db_session, series_id="WPS10000000", sector_code="20")
        resp = client.get("/api/v1/ppi?sector_code=10", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_measure_code(self, client: TestClient, db_session):
        seed_ppi(db_session, measure_code="01")
        resp = client.get("/api/v1/ppi?measure_code=01", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_duration_code(self, client: TestClient, db_session):
        seed_ppi(db_session, duration_code="01")
        seed_ppi(db_session, series_id="WPS00000001", duration_code="02")
        resp = client.get("/api/v1/ppi?duration_code=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["duration_code"] == "02"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_ppi(db_session, period="01")
        seed_ppi(db_session, series_id="WPS00000001", period="02")
        resp = client.get("/api/v1/ppi?period=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "02"


# ── JT ──────────────────────────────────────────────────────────────────────

class TestJTEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_jt(db_session)
        resp = client.get("/api/v1/jt", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_period_name_in_response(self, client: TestClient, db_session):
        seed_jt(db_session)
        resp = client.get("/api/v1/jt", headers=HEADERS)
        assert resp.json()["data"][0]["period_name"] == "January"

    def test_filter_by_state_code(self, client: TestClient, db_session):
        seed_jt(db_session, state_code="01")
        seed_jt(db_session, series_id="JT01000000000000000001", state_code="02")
        resp = client.get("/api/v1/jt?state_code=01", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_dataelement_code(self, client: TestClient, db_session):
        seed_jt(db_session, dataelement_code="JO")
        resp = client.get("/api/v1/jt?dataelement_code=JO", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_seasonal_code(self, client: TestClient, db_session):
        seed_jt(db_session, seasonal_code="S")
        seed_jt(db_session, series_id="JT00000000000000000001", seasonal_code="U")
        resp = client.get("/api/v1/jt?seasonal_code=U", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["seasonal_code"] == "U"

    def test_filter_by_sizeclass_code(self, client: TestClient, db_session):
        seed_jt(db_session, sizeclass_code="00")
        seed_jt(db_session, series_id="JT00000000000000000001", sizeclass_code="01")
        resp = client.get("/api/v1/jt?sizeclass_code=01", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["sizeclass_code"] == "01"

    def test_filter_by_ratelevel_code(self, client: TestClient, db_session):
        seed_jt(db_session, ratelevel_code="R")
        seed_jt(db_session, series_id="JT00000000000000000001", ratelevel_code="L")
        resp = client.get("/api/v1/jt?ratelevel_code=L", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["ratelevel_code"] == "L"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_jt(db_session, period="01")
        seed_jt(db_session, series_id="JT00000000000000000001", period="02")
        resp = client.get("/api/v1/jt?period=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "02"


# ── LA ──────────────────────────────────────────────────────────────────────

class TestLAEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_la(db_session)
        resp = client.get("/api/v1/la", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_filter_by_state_code(self, client: TestClient, db_session):
        seed_la(db_session, state_code="06")
        resp = client.get("/api/v1/la?state_code=06", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_measure_code(self, client: TestClient, db_session):
        seed_la(db_session, measure_code="03")
        resp = client.get("/api/v1/la?measure_code=03", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_area_type_code(self, client: TestClient, db_session):
        seed_la(db_session, area_type_code="1")
        seed_la(db_session, series_id="LAUST00000000000001", area_type_code="2")
        resp = client.get("/api/v1/la?area_type_code=2", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["area_type_code"] == "2"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_la(db_session, period="M01")
        seed_la(db_session, series_id="LAUST00000000000001", period="M02")
        resp = client.get("/api/v1/la?period=M02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "M02"


# ── CI ──────────────────────────────────────────────────────────────────────

class TestCIEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_ci(db_session)
        resp = client.get("/api/v1/ci", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_filter_by_industry_code(self, client: TestClient, db_session):
        seed_ci(db_session, industry_code="100000")
        resp = client.get("/api/v1/ci?industry_code=100000", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_occupation_code(self, client: TestClient, db_session):
        seed_ci(db_session, occupation_code="150000")
        resp = client.get("/api/v1/ci?occupation_code=150000", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_seasonal_code(self, client: TestClient, db_session):
        seed_ci(db_session, seasonal_code="U")
        seed_ci(db_session, series_id="CIU0000000000001", seasonal_code="S")
        resp = client.get("/api/v1/ci?seasonal_code=S", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["seasonal_code"] == "S"

    def test_filter_by_owner_code(self, client: TestClient, db_session):
        seed_ci(db_session, owner_code="00")
        seed_ci(db_session, series_id="CIU0000000000001", owner_code="01")
        resp = client.get("/api/v1/ci?owner_code=01", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["owner_code"] == "01"

    def test_filter_by_estimate_code(self, client: TestClient, db_session):
        seed_ci(db_session, estimate_code="01")
        seed_ci(db_session, series_id="CIU0000000000001", estimate_code="02")
        resp = client.get("/api/v1/ci?estimate_code=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["estimate_code"] == "02"

    def test_filter_by_periodicity_code(self, client: TestClient, db_session):
        seed_ci(db_session, periodicity_code="A")
        seed_ci(db_session, series_id="CIU0000000000001", periodicity_code="Q")
        resp = client.get("/api/v1/ci?periodicity_code=Q", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["periodicity_code"] == "Q"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_ci(db_session, period="01")
        seed_ci(db_session, series_id="CIU0000000000001", period="02")
        resp = client.get("/api/v1/ci?period=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "02"


# ── MP ──────────────────────────────────────────────────────────────────────

class TestMPEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_mp(db_session)
        resp = client.get("/api/v1/mp", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_period_name_in_response(self, client: TestClient, db_session):
        seed_mp(db_session)
        resp = client.get("/api/v1/mp", headers=HEADERS)
        assert resp.json()["data"][0]["period_name"] == "January"

    def test_filter_by_sector_code(self, client: TestClient, db_session):
        seed_mp(db_session, sector_code="10")
        resp = client.get("/api/v1/mp?sector_code=10", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_seasonal_code(self, client: TestClient, db_session):
        seed_mp(db_session, seasonal_code="S")
        seed_mp(db_session, series_id="MP0000000000001", seasonal_code="U")
        resp = client.get("/api/v1/mp?seasonal_code=U", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["seasonal_code"] == "U"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_mp(db_session, period="01")
        seed_mp(db_session, series_id="MP0000000000001", period="02")
        resp = client.get("/api/v1/mp?period=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "02"


# ── OE ──────────────────────────────────────────────────────────────────────

class TestOEEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_oe(db_session)
        resp = client.get("/api/v1/oe", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_period_name_in_response(self, client: TestClient, db_session):
        seed_oe(db_session)
        resp = client.get("/api/v1/oe", headers=HEADERS)
        assert resp.json()["data"][0]["period_name"] == "Annual"

    def test_filter_by_area_code(self, client: TestClient, db_session):
        seed_oe(db_session, area_code="0100000000")
        resp = client.get("/api/v1/oe?area_code=0100000000", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_sector_code(self, client: TestClient, db_session):
        seed_oe(db_session, sector_code="00")
        seed_oe(db_session, series_id="OEUS0000000000000000001", sector_code="01")
        resp = client.get("/api/v1/oe?sector_code=01", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["sector_code"] == "01"

    def test_filter_by_seasonal_code(self, client: TestClient, db_session):
        seed_oe(db_session, seasonal_code="U")
        seed_oe(db_session, series_id="OEUS0000000000000000001", seasonal_code="S")
        resp = client.get("/api/v1/oe?seasonal_code=S", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["seasonal_code"] == "S"

    def test_filter_by_areatype_code(self, client: TestClient, db_session):
        seed_oe(db_session, areatype_code="01")
        seed_oe(db_session, series_id="OEUS0000000000000000001", areatype_code="02")
        resp = client.get("/api/v1/oe?areatype_code=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["areatype_code"] == "02"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_oe(db_session, period="Annual")
        seed_oe(db_session, series_id="OEUS0000000000000000001", period="Q1")
        resp = client.get("/api/v1/oe?period=Q1", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "Q1"


# ── SA ──────────────────────────────────────────────────────────────────────

class TestSAEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_sa(db_session)
        resp = client.get("/api/v1/sa", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_period_name_in_response(self, client: TestClient, db_session):
        seed_sa(db_session)
        resp = client.get("/api/v1/sa", headers=HEADERS)
        assert resp.json()["data"][0]["period_name"] == "January"

    def test_filter_by_state_code(self, client: TestClient, db_session):
        seed_sa(db_session, state_code="06")
        resp = client.get("/api/v1/sa?state_code=06", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_seasonal_code(self, client: TestClient, db_session):
        seed_sa(db_session, seasonal_code="S")
        seed_sa(db_session, series_id="SAU0000000000001", seasonal_code="U")
        resp = client.get("/api/v1/sa?seasonal_code=U", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["seasonal_code"] == "U"

    def test_filter_by_detail_code(self, client: TestClient, db_session):
        seed_sa(db_session, detail_code="00")
        seed_sa(db_session, series_id="SAU0000000000001", detail_code="01")
        resp = client.get("/api/v1/sa?detail_code=01", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["detail_code"] == "01"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_sa(db_session, period="01")
        seed_sa(db_session, series_id="SAU0000000000001", period="02")
        resp = client.get("/api/v1/sa?period=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "02"


# ── SM ──────────────────────────────────────────────────────────────────────

class TestSMEndpoint:
    def test_basic_retrieval(self, client: TestClient, db_session):
        seed_sm(db_session)
        resp = client.get("/api/v1/sm", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_period_name_in_response(self, client: TestClient, db_session):
        seed_sm(db_session)
        resp = client.get("/api/v1/sm", headers=HEADERS)
        assert resp.json()["data"][0]["period_name"] == "January"

    def test_filter_by_supersector_code(self, client: TestClient, db_session):
        seed_sm(db_session, supersector_code="10")
        resp = client.get("/api/v1/sm?supersector_code=10", headers=HEADERS)
        assert resp.json()["total"] == 1

    def test_filter_by_data_type_code(self, client: TestClient, db_session):
        seed_sm(db_session, data_type_code="01")
        seed_sm(db_session, series_id="SMU0000000000001", data_type_code="02")
        resp = client.get("/api/v1/sm?data_type_code=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["data_type_code"] == "02"

    def test_filter_by_seasonal_code(self, client: TestClient, db_session):
        seed_sm(db_session, seasonal_code="S")
        seed_sm(db_session, series_id="SMU0000000000001", seasonal_code="U")
        resp = client.get("/api/v1/sm?seasonal_code=U", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["seasonal_code"] == "U"

    def test_filter_by_period(self, client: TestClient, db_session):
        seed_sm(db_session, period="01")
        seed_sm(db_session, series_id="SMU0000000000001", period="02")
        resp = client.get("/api/v1/sm?period=02", headers=HEADERS)
        body = resp.json()
        assert body["total"] == 1
        assert body["data"][0]["period"] == "02"
