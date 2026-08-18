<div align="center">

# AShareHub Python SDK

**Simple, Pythonic access to Chinese market data**

Query A-shares, ETFs, indices, financial statements, capital flows, real-time
quotes, news, and reference data from Python. Every endpoint returns a familiar
`pandas.DataFrame`.

[![PyPI version](https://img.shields.io/pypi/v/asharehub.svg)](https://pypi.org/project/asharehub/)
[![PyPI downloads](https://img.shields.io/pypi/dm/asharehub.svg)](https://pypi.org/project/asharehub/)
[![Python versions](https://img.shields.io/pypi/pyversions/asharehub.svg)](https://pypi.org/project/asharehub/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Website](https://asharehub.com) · [Documentation](https://asharehub.com/en/docs) · [API Reference](https://asharehub.com/en/docs/market-daily) · [Get an API Key](https://asharehub.com/en/console/register) · [Report an Issue](https://github.com/ChuYiCui1/AshareHub/issues)

</div>

---

AShareHub is the official open-source Python client for the hosted AShareHub
market data API. It gives analysts, researchers, and developers one consistent
interface for working with Chinese market data without maintaining their own
collection and normalization pipeline.

## Contents

- [Why AShareHub](#why-asharehub)
- [Quick start](#quick-start)
- [Data coverage](#data-coverage)
- [Common workflows](#common-workflows)
- [Data conventions](#data-conventions)
- [Client configuration](#client-configuration)
- [Error handling](#error-handling)
- [Documentation and ecosystem](#documentation-and-ecosystem)
- [Development](#development)
- [Contributing](#contributing)

## Why AShareHub

- **DataFrame first** — every public method returns a `pandas.DataFrame`, and
  an empty result returns an empty DataFrame.
- **One code convention** — stocks, indices, sectors, ETFs, and other
  instruments use the public `symbol` field consistently.
- **Broad market coverage** — use one client for prices, fundamentals,
  financial statements, flows, holdings, ETFs, real-time quotes, and news.
- **Discoverable contracts** — inspect request parameters and response fields
  locally through the packaged machine-readable public contract.
- **Small, familiar API** — install from PyPI, authenticate with one API key,
  and receive analysis-ready tabular results.

## Quick start

### 1. Install

```bash
pip install asharehub
```

AShareHub requires Python 3.10 or newer.

### 2. Get an API key

Create an account in the [AShareHub console](https://asharehub.com/en/console/register)
and generate an API key. Keep the key outside source control, for example in an
environment variable:

```bash
export ASHAREHUB_API_KEY="ash_your_key_here"
```

### 3. Query market data

```python
import os

from asharehub import AShareHub

with AShareHub(api_key=os.environ["ASHAREHUB_API_KEY"]) as client:
    daily = client.market_daily(
        symbol="000001.SZ",
        start_date="20240101",
        end_date="20241231",
    )

print(daily[["trade_date", "open", "high", "low", "close", "vol"]].head())
```

`daily` is a regular DataFrame, so it works directly with pandas, notebooks,
visualization libraries, and research pipelines.

## Data coverage

| Area | Examples | Selected SDK methods |
|---|---|---|
| Market and valuation | Daily OHLC, valuation ratios, adjustment factors, technical factors, price limits | `market_daily`, `fundamentals`, `adj_factor`, `technical_factors`, `limit_list` |
| Capital flows and holdings | Stock Connect flows, individual-stock money flow, northbound and southbound holdings | `moneyflow_hsgt`, `moneyflow`, `northbound_holdings`, `southbound_holdings` |
| Financials and corporate data | Statements, indicators, forecasts, dividends, audits, main business | `income`, `balance_sheet`, `cash_flow`, `financial_indicators`, `forecast`, `dividend` |
| Indices and concepts | Index prices and weights, concept sectors and constituents | `index_daily`, `index_weight`, `concepts`, `concept_members` |
| ETFs | Directory, prices, adjustment factors, NAV, shares, portfolios, baskets | `etf_basic`, `etf_daily`, `etf_nav`, `etf_portfolio`, `etf_sh_basket`, `etf_sz_basket` |
| Market activity | Margin data, block trades, top lists, institutional seats, shareholder activity | `margin`, `block_trade`, `top_list`, `top_inst`, `shareholders`, `holder_trade` |
| Reference and alternative data | Security lists, industries, calendars, chip distribution, FX | `stock_list`, `industry_list`, `trade_calendar`, `chip_distribution`, `fx_daily` |
| Live and research feeds | Real-time quotes, flash news, analyst reports | `realtime`, `news_flash`, `analyst_reports` |

See the [API documentation](https://asharehub.com/en/docs) for endpoint-specific
parameters, response schemas, and examples.

## Common workflows

### Compare an ETF with its benchmark

```python
with AShareHub(api_key=os.environ["ASHAREHUB_API_KEY"]) as client:
    etf = client.etf_daily(symbol="510300.SH", start_date="20240101")
    index = client.index_daily(symbol="000300.SH", start_date="20240101")
```

### Load financial statements

```python
with AShareHub(api_key=os.environ["ASHAREHUB_API_KEY"]) as client:
    income = client.income(symbol="600519.SH", period="20241231")
    balance_sheet = client.balance_sheet(symbol="600519.SH", period="20241231")
    cash_flow = client.cash_flow(symbol="600519.SH", period="20241231")
```

### Explore a concept sector and its constituents

```python
with AShareHub(api_key=os.environ["ASHAREHUB_API_KEY"]) as client:
    sectors = client.concepts(name="AI")
    members = client.concept_members(
        symbol="BK0425.DC",
        con_symbol="000001.SZ",
    )
```

### Fetch real-time quotes

```python
with AShareHub(api_key=os.environ["ASHAREHUB_API_KEY"]) as client:
    quotes = client.realtime(symbol="000001.SZ,600519.SH,510300.SH")
```

## Data conventions

### Instrument codes

Public instrument fields use one stable naming contract:

- Use `symbol` for the primary stock, index, Eastmoney sector, ETF, or other
  instrument code.
- Use `con_symbol` when a request or record contains a second constituent
  security.
- Use suffixed codes such as `000001.SZ`, `600519.SH`, `000300.SH`,
  `510300.SH`, or `BK0425.DC`.

This convention is shared by the REST API, Python SDK, MCP server, public
documentation, and packaged contract.

### Dates and results

- Dates use `YYYYMMDD`, for example `20240819`.
- The default `v2` client returns public fields such as `symbol` and native JSON
  numbers.
- Every method returns a DataFrame; no rows means `df.empty == True`.
- Method signatures vary intentionally. Use the contract or endpoint docs for
  the exact filters supported by each method.

### Inspect the public contract

The package includes the authoritative SDK/MCP method signatures, request
parameters, and response fields:

```python
from asharehub import PUBLIC_CONTRACT, get_contract

daily_contract = get_contract("market_daily")
print(daily_contract["request_parameters"])
print(daily_contract["response_fields"])
print(PUBLIC_CONTRACT["version"])
```

## Client configuration

Use the client as a context manager when possible so the underlying HTTP
connection is closed automatically:

```python
with AShareHub(
    api_key=os.environ["ASHAREHUB_API_KEY"],
    timeout=60.0,
) as client:
    data = client.market_daily(symbol="000001.SZ")
```

For development or a compatible deployment, provide a custom base URL:

```python
client = AShareHub(
    api_key=os.environ["ASHAREHUB_API_KEY"],
    base_url="https://your-api.example.com",
)
```

The client targets API `v2` by default. Existing integrations can explicitly
select the legacy response surface with `version="v1"`; public SDK method
parameters continue to use `symbol`.

## Error handling

HTTP errors are raised as `httpx.HTTPStatusError`, so standard httpx handling
works without an SDK-specific exception hierarchy:

```python
import httpx

try:
    data = client.market_daily(symbol="000001.SZ")
except httpx.HTTPStatusError as exc:
    if exc.response.status_code == 401:
        print("Check your API key")
    elif exc.response.status_code == 429:
        print("Rate limit reached")
    else:
        raise
```

## Authentication and usage limits

Requests authenticate through the `X-API-Key` header, which the SDK configures
from the `api_key` argument. A free tier is available; current quotas and paid
plans are maintained on the [pricing page](https://asharehub.com/en/console/pricing).

Never commit API keys to a repository, notebook, image, or issue report.

## Documentation and ecosystem

| Resource | Use it for |
|---|---|
| [Python SDK guide](https://asharehub.com/en/docs/sdk-install) | Installation and the first authenticated request |
| [REST API documentation](https://asharehub.com/en/docs) | Endpoint reference, schemas, authentication, and limits |
| [A-share market data](https://asharehub.com/en/docs/market-daily) | Prices, volume, adjustment factors, and trading data |
| [ETF data](https://asharehub.com/en/docs/etf-basic) | ETF reference data, prices, NAV, shares, portfolios, and baskets |
| [Financial data](https://asharehub.com/en/docs/financials) | Statements, indicators, forecasts, and dividends |
| [MCP server](https://asharehub.com/en/docs/mcp-setup) | Connecting MCP-compatible clients and AI agents |
| [Agent Skill](https://asharehub.com/en/skill) | Guided AShareHub workflows for coding agents |

## Development

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/ChuYiCui1/AshareHub.git
cd AShareHub
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
```

Tests that require a live API are skipped unless both environment variables are
set. When an API server is available, run the integration suite with:

```bash
ASHAREHUB_API_KEY="ash_your_key_here" \
ASHAREHUB_BASE_URL="http://localhost:8000" \
pytest -v
```

## Contributing

Issues and pull requests are welcome. Before opening a change:

1. Search [existing issues](https://github.com/ChuYiCui1/AshareHub/issues) for
   related work.
2. Keep the public `symbol` / `con_symbol` compatibility contract intact.
3. Add or update tests for behavior changes.
4. Run `pytest -q` and describe the user-visible impact in the pull request.

For questions, bug reports, or endpoint requests, open a
[GitHub issue](https://github.com/ChuYiCui1/AshareHub/issues).

## Releases and support

- Install releases from [PyPI](https://pypi.org/project/asharehub/).
- Review version history on [GitHub Releases](https://github.com/ChuYiCui1/AshareHub/releases).
- Read the [documentation](https://asharehub.com/en/docs).
- Contact `support@asharehub.com` for account or service support.

## License

The SDK is available under the [MIT License](LICENSE).

## Disclaimer

AShareHub provides data access tooling, not investment advice. Verify data,
licensing requirements, and applicable terms before using it in research,
production systems, or trading decisions.

---

<div align="center">

**Built for the global investment community**

[asharehub.com](https://asharehub.com)

</div>
