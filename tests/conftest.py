"""Shared test fixtures: SQLite in-memory database, TestClient, seed data."""

import os
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Must set env vars BEFORE importing app modules that call get_settings() at
# module level (app.database, app.config, app.main).
os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
os.environ.setdefault("API_KEYS", "test-key-123")
os.environ.setdefault("RATE_LIMIT", "1000/minute")

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import (  # noqa: E402
    CEData,
    CPIData,
    PPIData,
    JTData,
    LAData,
    CIData,
    MPData,
    OEData,
    SAData,
    SMData,
)

# ---------------------------------------------------------------------------
# In-memory SQLite engine & session factory
#
# StaticPool keeps a single connection alive so that tables created in one
# session are visible to all others (default :memory: DBs are per-connection).
# ---------------------------------------------------------------------------
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# SQLite doesn't enforce foreign keys by default; enable it.
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the app's get_db dependency so every request uses the test DB.
app.dependency_overrides[get_db] = override_get_db


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client() -> TestClient:
    """FastAPI test client with the DB dependency overridden."""
    return TestClient(app)


@pytest.fixture()
def db_session():
    """Raw SQLAlchemy session for seeding data in tests."""
    session = TestingSessionLocal()
    yield session
    session.close()


# ---------------------------------------------------------------------------
# Seed helpers – one per model
# ---------------------------------------------------------------------------

def seed_ce(session, **overrides):
    defaults = dict(
        series_id="CEU0000000001",
        year=2023,
        period="01",
        period_name="January",
        value=Decimal("100.50"),
        supersector_code="00",
        supersector_name="Total nonfarm",
        industry_code="000000",
        industry_name="Total nonfarm",
        datatype_code="01",
        datatype_name="All employees",
        seasonal_code="S",
        seasonal_name="Seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = CEData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_cpi(session, **overrides):
    defaults = dict(
        series_id="CUSR0000SA0",
        year=2023,
        period="M01",
        period_name="January",
        value=Decimal("299.170"),
        area_code="0000",
        area_name="U.S. city average",
        item_code="SA0",
        item_name="All items",
        seasonal_code="S",
        seasonal_text="Seasonally adjusted",
    )
    defaults.update(overrides)
    obj = CPIData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_ppi(session, **overrides):
    defaults = dict(
        series_id="WPS00000000",
        year=2023,
        period="01",
        period_name="January",
        value=Decimal("100.0000"),
        measure_code="01",
        measure_name="Index",
        sector_code="00",
        sector_name="Total",
        class_code="00",
        class_name="Total",
        duration_code="01",
        duration_name="Monthly",
        seasonal_code="S",
        seasonal_name="Seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = PPIData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_jt(session, **overrides):
    defaults = dict(
        series_id="JT00000000000000000000",
        year=2023,
        period="01",
        period_name="January",
        value=Decimal("10000.00"),
        industry_code="000000",
        industry_name="Total nonfarm",
        state_code="00",
        state_name="Total",
        area_code="0000000000",
        area_name="Total",
        sizeclass_code="00",
        sizeclass_name="Total",
        dataelement_code="JO",
        dataelement_name="Job openings",
        ratelevel_code="R",
        ratelevel_name="Rate",
        seasonal_code="S",
        seasonal_name="Seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = JTData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_la(session, **overrides):
    defaults = dict(
        series_id="LAUST00000000000000",
        year=2023,
        period="M01",
        value=Decimal("5.50"),
        area_type_code="1",
        area_type_name="State",
        area_code="0000000000000",
        area_name="Total",
        measure_code="03",
        measure_name="Unemployment rate",
        seasonal_code="S",
        seasonal_name="Seasonally adjusted",
        state_code="00",
        state_name="Total",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = LAData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_ci(session, **overrides):
    defaults = dict(
        series_id="CIU0000000000000",
        year=2023,
        period="01",
        value=Decimal("50000.00"),
        owner_code="00",
        owner_name="Total",
        industry_code="000000",
        industry_name="Total",
        occupation_code="000000",
        occupation_name="Total",
        area_code="0000000000",
        area_name="Total",
        estimate_code="01",
        estimate_name="Mean wage",
        periodicity_code="A",
        periodicity_name="Annual",
        seasonal_code="U",
        seasonal_name="Not seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = CIData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_mp(session, **overrides):
    defaults = dict(
        series_id="MP0000000000000",
        year=2023,
        period="01",
        period_name="January",
        value=Decimal("500.00"),
        sector_code="00",
        sector_name="Total",
        measure_code="01",
        measure_name="Initial claims",
        duration_code="01",
        duration_name="Monthly",
        seasonal_code="S",
        seasonal_name="Seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = MPData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_oe(session, **overrides):
    defaults = dict(
        series_id="OEUS0000000000000000000",
        year=2023,
        period="Annual",
        period_name="Annual",
        value=Decimal("55000.00"),
        areatype_code="01",
        areatype_name="National",
        area_code="0000000000",
        area_name="Total",
        industry_code="000000",
        industry_name="Total",
        occupation_code="000000",
        occupation_name="Total",
        datatype_code="01",
        datatype_name="Employment",
        sector_code="00",
        sector_name="Total",
        seasonal_code="U",
        seasonal_name="Not seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = OEData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_sa(session, **overrides):
    defaults = dict(
        series_id="SAU0000000000000",
        year=2023,
        period="01",
        period_name="January",
        value=Decimal("150000.00"),
        state_code="00",
        state_name="Total",
        area_code="0000000000",
        area_name="Total",
        industry_code="000000",
        industry_name="Total",
        detail_code="00",
        detail_name="Total",
        data_type_code="01",
        data_type_name="All employees",
        seasonal_code="S",
        seasonal_name="Seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = SAData(**defaults)
    session.add(obj)
    session.commit()
    return obj


def seed_sm(session, **overrides):
    defaults = dict(
        series_id="SMU0000000000000",
        year=2023,
        period="01",
        period_name="January",
        value=Decimal("140000.00"),
        state_code="00",
        state_name="Total",
        area_code="0000000000",
        area_name="Total",
        supersector_code="00",
        supersector_name="Total nonfarm",
        industry_code="000000",
        industry_name="Total nonfarm",
        data_type_code="01",
        data_type_name="All employees",
        seasonal_code="S",
        seasonal_name="Seasonally adjusted",
        footnote_codes=None,
    )
    defaults.update(overrides)
    obj = SMData(**defaults)
    session.add(obj)
    session.commit()
    return obj
