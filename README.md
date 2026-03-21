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
- 🚀 Simple, intuitive API
- 📊 Comprehensive market data coverage
- 🔒 Secure authentication
- ⚡ Fast and reliable
- 📈 10+ years of historical data
- 🐍 Type-safe with Pydantic models

---

## Installation

```bash
pip install asharehub
```

**Requirements:** Python 3.10+

---

## Quick Start

```python
from asharehub import AShareHub

# Initialize client
client = AShareHub(api_key="ash_your_key_here")

# Get daily market data
data = client.market_daily(
    ts_code="000001.SZ",
    start_date="2024-01-01",
    end_date="2024-12-31",
    limit=100
)

# Access data
for bar in data:
    print(f"{bar.trade_date}: {bar.close}")
```

---

## API Methods

### Market Data

#### `market_daily()`
Get daily OHLCV price data for A-share stocks.

```python
data = client.market_daily(
    ts_code="000001.SZ",      # Stock code (optional)
    start_date="2024-01-01",  # Start date (optional)
    end_date="2024-12-31",    # End date (optional)
    limit=100,                # Max rows (default: 100)
    offset=0                  # Pagination offset (default: 0)
)
```

**Returns:** List of `DailyBar` objects with fields: `ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`

#### `fundamentals()`
Get daily fundamental indicators (PE, PB, turnover rate, market cap).

```python
data = client.fundamentals(
    ts_code="000001.SZ",
    start_date="2024-01-01",
    limit=100
)
```

**Returns:** List of `Fundamentals` objects with valuation metrics

---

### Capital Flows

#### `northbound_flows()`
Get northbound capital flows via Stock Connect (Shanghai-HK and Shenzhen-HK).

```python
flows = client.northbound_flows(
    start_date="2024-01-01",
    end_date="2024-01-31",
    limit=100
)
```

**Returns:** List of `NorthboundFlow` objects with fields: `trade_date`, `north_money`, `south_money`, `ggt_ss`, `ggt_sz`

---

### Financials

#### `financial_indicators()`
Get quarterly financial indicators (ROE, margins, EPS, 50+ metrics).

```python
financials = client.financial_indicators(
    ts_code="000001.SZ",art_date="2024-01-01",
    limit=20
)
```

**Returns:** List of `FinaIndicator` objects with comprehensive financial metrics

---

### Indices

#### `index_daily()`
Get daily OHLCV data for major Chinese market indices.

```python
indices = client.index_daily(
    ts_code="000001.SH",  # Default: SSE Composite
    start_date="2024-01-01",
    limit=100
)
```

**Common Index Codes:**
- `000001.SH` - SSE Composite (上证综指)
- `000300.SH` - CSI 300 (沪深300)
- `399001.SZ` - SZSE Component (深证成指)
- `399006.SZ` - ChiNext (创业板指)
- `000016.SH` - SSE 50 (上证50)

---

### Microstructure

#### `chip_distribution()`
Get chip distribution data (cost basis and winner rates).

```python
chips = client.chip_distribution(
    ts_code="000001.SZ",
    start_date="2024-01-01",
    limit=100
)
```

**Returns:** List of `ChipDistribution` objects with cost percentiles and winner rates

---

### Reference Data

#### `fx_daily()`
Get daily FX rates with bid/ask prices.

```python
fx = client.fx_daily(
    ts_code="USDCNH.FXCM",  # Default: USD/CNH
    start_date="2024-01-01",
    limit=100
)
```

**Returns:** List of `FxDaily` objectsth bid/ask OHLC data

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
    data = client.market_daily(ts_code="000001.SZ")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.statusde == 429:
        print("Rate limit exceeded")
    else:
        print(f"HTTP error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

---

## Advanced Usage

### Context Manager

```python
with AShareHub(api_key="your_key") as client:
    data = client.market_daily(ts_code="000001.SZ")
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
| | 100 requests |
| Pro | $49/month | 10,000 requests |
| Business | $99/month | 50,000 requests |

---

## Support

- 📖 [Documentation](https://asharehub.com/docs)
- 🐛 [Report Issues](https://github.com/ChuYiCui1/AshareHub/issues)
- 💬 Email: support@asharehub.com

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for the global investment community**

[asharehub.com](https://asharehub.com)

</div>
