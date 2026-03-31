<div align="center">

# AShareHub Python SDK

**Official Python SDK for Chinese A-Share Market Data**

[![PyPI version](https://img.shields.io/pypi/v/asharehub.svg)](https://pypi.org/project/asharehub/)
[![Python versions](https://img.shields.io/pypi/pyversions/asharehub.svg)](https://pypi.org/project/asharehub/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Website](https://asharehub.com) • [Documentation](https://asharehub.com/docs) • [API Reference](https://asharehub.com/docs#api-reference) • [Get API Key](https://asharehub.com/console/register)

</div>

---

## Overview

AShareHub provides institutional-grade Chinese A-Share market data through a simple, modern Python SDK. Access real-time and historical data for 5,000+ stocks on Shanghai and Shenzhen exchanges.

**Key Features:**
- Returns `pd.DataFrame` — same convention as Tushare
- 29 data endpoints covering market, financial, and reference data
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
df = client.market_daily(ts_code="000001.SZ", start_date="2024-01-01", end_date="2024-12-31")
print(df[["trade_date", "open", "high", "low", "close", "vol"]])

client.close()
```

---

## API Methods

All methods return `pd.DataFrame`. Empty results return an empty DataFrame (`df.empty == True`).

### Market Data

```python
df = client.market_daily(ts_code="000001.SZ", start_date="2024-01-01")
df = client.fundamentals(ts_code="000001.SZ", start_date="2024-01-01")
df = client.margin(ts_code="000001.SZ", limit=100)
df = client.block_trade(ts_code="000001.SZ", limit=100)
df = client.top_list(limit=100)
df = client.shareholders(ts_code="000001.SZ", limit=100)
df = client.holder_trade(ts_code="000001.SZ", limit=100)
df = client.concepts(limit=100)
df = client.concept_members(ts_code="TS2", limit=100)
df = client.adj_factor(ts_code="000001.SZ", limit=100)
df = client.technical_factors(ts_code="000001.SZ", limit=100)
df = client.limit_list(limit_type="U", limit=100)
```

### Capital Flows

```python
df = client.northbound_flows(start_date="2024-01-01", limit=100)
df = client.moneyflow(ts_code="000001.SZ", limit=100)
df = client.northbound_holdings(ts_code="000001.SZ", limit=100)
```

### Financials

```python
df = client.financial_indicators(ts_code="000001.SZ", limit=20)
df = client.income(ts_code="000001.SZ", limit=20)
df = client.balance_sheet(ts_code="000001.SZ", limit=20)
df = client.cash_flow(ts_code="000001.SZ", limit=20)
df = client.forecast(ts_code="000001.SZ", limit=50)
df = client.express(ts_code="000001.SZ", limit=50)
df = client.dividend(ts_code="000001.SZ", limit=50)
```

### Indices

```python
df = client.index_daily(ts_code="000300.SH", start_date="2024-01-01")
df = client.index_weight(index_code="399300.SZ", limit=100)
```

### Other

```python
df = client.chip_distribution(ts_code="000001.SZ", limit=100)
df = client.fx_daily(ts_code="USDCNH.FXCM", limit=100)
```

### Reference Data

```python
df = client.stock_list(limit=100)
df = client.industry_list(limit=100)
df = client.trade_calendar(exchange="SSE", start_date="2024-01-01")
```

---

## Common Parameters

All data methods accept:

| Parameter | Type | Description |
|-----------|------|-------------|
| `ts_code` | str | Stock/index code, e.g. `000001.SZ` |
| `start_date` | str | Start date, `YYYY-MM-DD` |
| `end_date` | str | End date, `YYYY-MM-DD` |
| `limit` | int | Max rows per request |
| `offset` | int | Pagination offset |

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

1. Visit [asharehub.com/console/register](https://asharehub.com/console/register)
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
    df = client.market_daily(ts_code="000001.SZ")
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
    df = client.market_daily(ts_code="000001.SZ")
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

- [Documentation](https://asharehub.com/docs)
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
