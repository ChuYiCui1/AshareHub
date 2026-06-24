"""SDK integration tests — runs against a live API server.

Start the API first:
    cd api && uvicorn app.main:app --port 8000

Then run:
    cd sdk && pytest -v

Every client method returns a pandas DataFrame (since v0.3.0), so tests assert
on DataFrame shape and columns (df.iloc[0]["col"]), not on model-instance
attributes.
"""
import os
import pytest
import pandas as pd
from asharehub import AShareHub

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
def test_market_daily(client):
    df = client.market_daily(symbol="000001.SZ", limit=3)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "close" in df.columns
    assert df.iloc[0]["ts_code"] == "000001.SZ"


@requires_server
def test_fundamentals(client):
    df = client.fundamentals(symbol="000001.SZ", limit=3)
    assert len(df) > 0
    assert "pe_ttm" in df.columns


@requires_server
def test_moneyflow_hsgt(client):
    df = client.moneyflow_hsgt(limit=3)
    assert len(df) > 0
    assert df.iloc[0]["north_money"] is not None


@requires_server
def test_chip_distribution(client):
    df = client.chip_distribution(symbol="000001.SZ", limit=3)
    assert len(df) > 0
    assert "winner_rate" in df.columns


@requires_server
def test_fx_daily(client):
    df = client.fx_daily(limit=3)
    assert len(df) > 0
    assert df.iloc[0]["ts_code"] == "USDCNH.FXCM"


@requires_server
def test_index_daily(client):
    df = client.index_daily(limit=3)
    assert len(df) > 0
    assert df.iloc[0]["ts_code"] == "000001.SH"


@requires_server
def test_financial_indicators(client):
    df = client.financial_indicators(symbol="000001.SZ", limit=3)
    assert len(df) > 0
    assert "roe" in df.columns
