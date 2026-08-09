<div align="center">

# AShareHub Python SDK

**Official Python SDK for Chinese A-Share, ETF and Hong Kong Market Data**

[![PyPI version](https://img.shields.io/pypi/v/asharehub.svg)](https://pypi.org/project/asharehub/)
[![Python versions](https://img.shields.io/pypi/pyversions/asharehub.svg)](https://pypi.org/project/asharehub/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Website](https://asharehub.com) • [Documentation](https://asharehub.com/en/docs) • [API Reference](https://asharehub.com/en/docs/market-daily) • [MCP & Skill](https://asharehub.com/en/skill) • [Get API Key](https://asharehub.com/en/console/register)

</div>

---

## Overview

AShareHub provides Chinese A-share, ETF and Hong Kong market data through a simple, modern Python SDK.

**Key Features:**
- Returns `pd.DataFrame` — same convention as Tushare
- 50 data endpoints covering A-shares, ETFs, Hong Kong stocks, financials, real-time, news, and reference data
- 10+ years of historical data
- Secure API key authentication
- Fast and reliable

---

## Installation

```bash
pip install asharehub
```

**Requirements:** Python 3.10+, pandas

---

## Quick Start

```python
from asharehub import AShareHub

client = AShareHub(api_key="ash_your_key_here")

# Get daily market data — returns pd.DataFrame
df = client.market_daily(symbol="000001.SZ", start_date="20240101", end_date="20241231")
print(df[["trade_date", "open", "high", "low", "close", "vol"]])

client.close()
```

---

## API Methods

All methods return `pd.DataFrame`. Empty results return an empty DataFrame (`df.empty == True`).
The packaged `PUBLIC_CONTRACT` contains every REST path, SDK/MCP signature,
request parameter and response field:

```python
from asharehub import get_contract

daily_contract = get_contract("market_daily")
print(daily_contract["response_fields"])
```

### Market Data

```python
df = client.market_daily(symbol="000001.SZ", start_date="20240101")
df = client.fundamentals(symbol="000001.SZ", start_date="20240101")
df = client.margin(symbol="000001.SZ")
df = client.block_trade(symbol="000001.SZ")
df = client.top_list()
df = client.shareholders(symbol="000001.SZ")
df = client.holder_trade(symbol="000001.SZ")
df = client.concepts()
df = client.concept_members(symbol="BK0425.DC", con_symbol="000001.SZ")
df = client.adj_factor(symbol="000001.SZ")
df = client.technical_factors(symbol="000001.SZ")
df = client.limit_list(limit_type="U")
```

### Capital Flows

```python
df = client.moneyflow_hsgt(start_date="20240101")
df = client.moneyflow(symbol="000001.SZ")
df = client.northbound_holdings(symbol="000001.SZ")
```

### Financials

```python
df = client.financial_indicators(symbol="000001.SZ")
df = client.income(symbol="000001.SZ")
df = client.balance_sheet(symbol="000001.SZ")
df = client.cash_flow(symbol="000001.SZ")
df = client.forecast(symbol="000001.SZ")
df = client.express(symbol="000001.SZ")
df = client.dividend(symbol="000001.SZ")
```

### Indices

```python
df = client.index_daily(symbol="000300.SH", start_date="20240101")
df = client.index_weight(symbol="399300.SZ")
```

### ETFs

```python
df = client.etf_basic(list_status="L")
df = client.etf_indices()
df = client.etf_daily(symbol="510300.SH", start_date="20260101")
df = client.etf_adj_factor(symbol="510300.SH", start_date="20260101")
df = client.etf_share_size(symbol="510300.SH", start_date="20260101")
df = client.etf_nav(symbol="510300.SH", start_date="20260101")
df = client.etf_portfolio(symbol="510300.SH", period="20260331")
```

### Hong Kong Stocks

```python
# Five-digit symbols with the .HK suffix
stocks = client.hk_stock_list(list_status="L")
daily = client.hk_daily(symbol="00700.HK", start_date="20260101")
calendar = client.hk_trade_calendar(start_date="20260101", is_open=1)
```

Hong Kong daily prices are unadjusted. Prices and turnover are in HKD; volume is in shares.

### Other

```python
df = client.chip_distribution(symbol="000001.SZ")
df = client.fx_daily(symbol="USDCNH.FXCM")
```

### Reference Data

```python
df = client.stock_list()
df = client.industry_list()
df = client.trade_calendar(exchange="SSE", start_date="20240101")
```

---

## Common Parameters

Most instrument/date-series methods accept some or all of the following. Use
`get_contract(method)` for the exact signature; market-wide, reference, news and
calendar interfaces intentionally differ.

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | str | Suffixed stock/index/ETF/HK code, e.g. `000001.SZ` or `00700.HK` |
| `start_date` | str | Start date, `YYYYMMDD` |
| `end_date` | str | End date, `YYYYMMDD` |

---

## Common Index Codes

| Code | Name |
|------|------|
| `000001.SH` | SSE Composite (上证综指) |
| `000300.SH` | CSI 300 (沪深300) |
| `399001.SZ` | SZSE Component (深证成指) |
| `399006.SZ` | ChiNext (创业板指) |
| `000016.SH` | SSE 50 (上证50) |

---

## Authentication

Get your free API key:

1. Visit [asharehub.com/en/console/register](https://asharehub.com/en/console/register)
2. Create an account
3. Generate your API key in the dashboard

**Free tier includes 100 API calls per day.**

---

## Error Handling

```python
from asharehub import AShareHub
import httpx

client = AShareHub(api_key="your_key")

try:
    df = client.market_daily(symbol="000001.SZ")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")
    else:
        print(f"HTTP error: {e}")
```

---

## Advanced Usage

### Context Manager

```python
with AShareHub(api_key="your_key") as client:
    df = client.market_daily(symbol="000001.SZ")
    # Client automatically closes when exiting context
```

### Custom Base URL

```python
client = AShareHub(
    api_key="your_key",
    base_url="https://custom.api.url",
    timeout=60.0
)
```

---

## Rate Limits

| Plan | Price | Daily Limit |
|------|-------|-------------|
| Free | $0 | 100 requests |
| Pro | $49/month | 10,000 requests |
| Business | $99/month | 50,000 requests |

---

## Support

- [Documentation](https://asharehub.com/en/docs)
- [MCP & Agent Skill](https://asharehub.com/en/skill)
- [Report Issues](https://github.com/ChuYiCui1/AshareHub/issues)
- Email: support@asharehub.com

---

## License

MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built for the global investment community**

[asharehub.com](https://asharehub.com)

</div>
