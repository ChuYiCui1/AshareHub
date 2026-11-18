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
import inspect
import pytest
import pandas as pd
from asharehub import AShareHub, PUBLIC_CONTRACT, get_contract, __version__
from asharehub.models import MODEL_BY_METHOD

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
    assert __version__ == "0.10.0"


def test_unreleased_hk_market_methods_are_not_public():
    for method in ("hk_stock_list", "hk_daily", "hk_trade_calendar"):
        assert not hasattr(AShareHub, method)


def test_concept_methods_keep_public_symbol_contract():
    concepts = inspect.signature(AShareHub.concepts).parameters
    members = inspect.signature(AShareHub.concept_members).parameters

    assert "symbol" in concepts and "bk_code" not in concepts
    assert {"symbol", "con_symbol"} <= set(members)
    assert "bk_code" not in members and "con_code" not in members
    assert AShareHub._V2_PARAM_RENAME["con_code"] == "con_symbol"


def test_machine_readable_contract_matches_sdk_methods_and_models():
    interfaces = PUBLIC_CONTRACT["interfaces"]
    assert PUBLIC_CONTRACT["version"] == "v2"
    assert len(interfaces) == 50
    assert set(MODEL_BY_METHOD) == set(interfaces)

    for method, entry in interfaces.items():
        signature = inspect.signature(getattr(AShareHub, method)).parameters
        assert [name for name in signature if name != "self"] == entry["request_parameters"]
        assert list(MODEL_BY_METHOD[method].model_fields) == entry["response_fields"]
        assert not {"ts_code", "index_code", "con_code"} & set(entry["response_fields"])

    assert get_contract("concept_members")["response_fields"][:3] == [
        "trade_date", "symbol", "con_symbol",
    ]
    assert get_contract("etf_basic")["response_fields"][4] == "index_symbol"


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

@pytest.mark.parametrize('method,args,path', [
    ('institutional_surveys', {'event_id': 'a'*64, 'include_content': True, 'limit': 1, 'offset': 2}, 'institutional-surveys'),
    ('survey_participants', {'rece_org': '甲机构', 'org_type': '基金', 'limit': 2}, 'survey-participants'),
    ('broker_recommendations', {'month': '202611', 'broker': '券商甲'}, 'broker-recommendations'),
])
def test_research_request_serialization(method, args, path):
    import httpx
    seen = []
    def handle(request):
        seen.append(request)
        return httpx.Response(200, json=[{'month': '202611', 'event_id': '1'*64, 'content': '12345', 'symbol': '000001.SZ'}])
    with AShareHub(api_key='test') as client:
        client._client.close()
        client._client = httpx.Client(base_url='https://test', transport=httpx.MockTransport(handle))
        frame = getattr(client, method)(**args)
    assert seen[0].url.path == '/v2/research/' + path
    for name, value in args.items():
        assert seen[0].url.params[name] == (str(value).lower() if isinstance(value, bool) else str(value))
    assert frame.iloc[0]['month'] == '202611'
    assert frame.iloc[0]['event_id'] == '1'*64
    assert frame.iloc[0]['content'] == '12345'
    with AShareHub(api_key='test', version='v1') as client:
        with pytest.raises(ValueError, match='requires version'):
            getattr(client, method)(**args)
