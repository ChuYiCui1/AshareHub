"""SDK integration tests — runs against a live API server.

Start the API first:
    cd api && uvicorn app.main:app --port 8000

Then run:
    cd sdk && ASHAREHUB_API_KEY=... ASHAREHUB_BASE_URL=http://localhost:8000 pytest -v

Every client method returns a pandas DataFrame (since v0.3.0), so tests assert
on DataFrame shape and columns (df.iloc[0]["col"]), not on model-instance
attributes.
"""
import os
import pytest
import pandas as pd
from asharehub import AShareHub, __version__

API_KEY = os.getenv("ASHAREHUB_API_KEY", "")
BASE_URL = os.getenv("ASHAREHUB_BASE_URL", "http://localhost:8000")

requires_server = pytest.mark.skipif(
    not API_KEY or not os.getenv("ASHAREHUB_BASE_URL"),
    reason="ASHAREHUB_API_KEY/ASHAREHUB_BASE_URL not set for live integration tests",
)


@pytest.fixture(scope="module")
def client():
    c = AShareHub(api_key=API_KEY, base_url=BASE_URL)
    yield c
    c.close()


def test_sdk_version():
    assert __version__ == "0.8.0"


@requires_server
def test_market_daily(client):
    df = client.market_daily(symbol="000001.SZ")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "close" in df.columns
    assert df.iloc[0]["symbol"] == "000001.SZ"


@requires_server
def test_fundamentals(client):
    df = client.fundamentals(symbol="000001.SZ")
    assert len(df) > 0
    assert "pe_ttm" in df.columns


@requires_server
def test_moneyflow_hsgt(client):
    df = client.moneyflow_hsgt()
    assert len(df) > 0
    assert df.iloc[0]["north_money"] is not None


@requires_server
def test_chip_distribution(client):
    df = client.chip_distribution(symbol="000001.SZ")
    assert len(df) > 0
    assert "winner_rate" in df.columns


@requires_server
def test_fx_daily(client):
    df = client.fx_daily()
    assert len(df) > 0
    assert df.iloc[0]["symbol"] == "USDCNH.FXCM"


@requires_server
def test_index_daily(client):
    df = client.index_daily()
    assert len(df) > 0
    assert df.iloc[0]["symbol"] == "000001.SH"


@requires_server
def test_financial_indicators(client):
    df = client.financial_indicators(symbol="000001.SZ")
    assert len(df) > 0
    assert "roe" in df.columns


@requires_server
def test_etf_basic(client):
    df = client.etf_basic(symbol="510300.SH")
    assert len(df) > 0
    assert df.iloc[0]["symbol"] == "510300.SH"
    assert "mgr_name" in df.columns


@requires_server
def test_etf_daily(client):
    df = client.etf_daily(symbol="510300.SH")
    assert len(df) > 0
    assert df.iloc[0]["symbol"] == "510300.SH"
    assert "close" in df.columns
