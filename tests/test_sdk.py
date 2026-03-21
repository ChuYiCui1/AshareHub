"""SDK integration tests — runs against a live API server.

Start the API first:
    cd api && uvicorn app.main:app --port 8000

Then run:
    cd sdk && pytest -v
"""
import os
import pytest
from asharehub import AShareHub
from asharehub.models import (
    DailyBar, Fundamentals, NorthboundFlow,
    ChipDistribution, FxDaily, IndexDaily, FinaIndicator,
)

API_KEY = os.getenv("ASHAREHUB_API_KEY", "")
BASE_URL = os.getenv("ASHAREHUB_BASE_URL", "http://localhost:8000")

requires_server = pytest.mark.skipif(
    not API_KEY, reason="ASHAREHUB_API_KEY not set"
)


@pytest.fixture(scope="module")
def client():
    c = AShareHub(api_key=API_KEY, base_url=BASE_URL)
    yield c
    c.close()


@requires_server
def test_daily(client):
    bars = client.daily(ts_code="000001.SZ", limit=3)
    assert len(bars) > 0
    assert isinstance(bars[0], DailyBar)
    assert bars[0].ts_code == "000001.SZ"


@requires_server
def test_fundamentals(client):
    rows = client.fundamentals(ts_code="000001.SZ", limit=3)
    assert len(rows) > 0
    assert isinstance(rows[0], Fundamentals)


@requires_server
def test_northbound(client):
    rows = client.northbound(limit=3)
    assert len(rows) > 0
    assert isinstance(rows[0], NorthboundFlow)
    assert rows[0].north_money is not None


@requires_server
def test_chips(client):
    rows = client.chips(ts_code="000001.SZ", limit=3)
    assert len(rows) > 0
    assert isinstance(rows[0], ChipDistribution)


@requires_server
def test_fx(client):
    rows = client.fx(limit=3)
    assert len(rows) > 0
    assert isinstance(rows[0], FxDaily)
    assert rows[0].ts_code == "USDCNH.FXCM"


@requires_server
def test_indices(client):
    rows = client.indices(limit=3)
    assert len(rows) > 0
    assert isinstance(rows[0], IndexDaily)
    assert rows[0].ts_code == "000001.SH"


@requires_server
def test_financials(client):
    rows = client.financials(ts_code="000001.SZ", limit=3)
    assert len(rows) > 0
    assert isinstance(rows[0], FinaIndicator)
    assert rows[0].roe is not None
