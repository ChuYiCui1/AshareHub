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
    assert __version__ == "0.9.0"


def test_hk_methods_target_expected_paths():
    client = object.__new__(AShareHub)
    calls = []
    client._get = lambda path, params: calls.append((path, params)) or pd.DataFrame()

    client.hk_stock_list(symbol="00700.HK", list_status="L")
    client.hk_daily(symbol="00700.HK", trade_date="20260807")
    client.hk_trade_calendar(start_date="20260801", end_date="20260808", is_open=1)

    assert [path for path, _ in calls] == [
        "/v1/hk/basic",
        "/v1/hk/daily",
        "/v1/hk/trade-calendar",
    ]
    assert calls[0][1] == {"ts_code": "00700.HK", "list_status": "L"}
    assert calls[1][1]["trade_date"] == "20260807"


def test_concept_methods_keep_con_code_and_bk_code_separate():
    client = object.__new__(AShareHub)
    client._version = "v2"
    calls = []
    client._get = lambda path, params: calls.append((path, params)) or pd.DataFrame()

    client.concepts(bk_code="BK0949.DC", trade_date="20260807")
    client.concept_members(
        bk_code="BK0949.DC", con_code="000001.SZ", trade_date="20260807"
    )

    assert calls[0][1]["bk_code"] == "BK0949.DC"
    assert "symbol" not in calls[0][1]
    assert calls[1][1]["bk_code"] == "BK0949.DC"
    assert calls[1][1]["con_code"] == "000001.SZ"
    assert "symbol" not in calls[1][1]
    assert "con_symbol" not in calls[1][1]


def test_v1_concept_methods_preserve_tushare_parameter_names():
    client = object.__new__(AShareHub)
    client._version = "v1"
    calls = []
    client._get = lambda path, params: calls.append((path, params)) or pd.DataFrame()

    client.concept_members(bk_code="BK0949.DC", con_code="000001.SZ")

    assert calls[0][1]["ts_code"] == "BK0949.DC"
    assert calls[0][1]["con_code"] == "000001.SZ"


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


@requires_server
def test_hk_daily(client):
    df = client.hk_daily(symbol="00700.HK")
    assert len(df) > 0
    assert df.iloc[0]["symbol"] == "00700.HK"
    assert "close" in df.columns
