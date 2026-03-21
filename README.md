# AShareHub Python SDK

Official Python SDK for [AShareHub](https://asharehub.com) — Chinese A-Share market data API.

## Installation

```bash
pip install asharehub
```

## Quick Start

```python
from asharehub import AShareHub

# Initialize client with your API key
client = AShareHub(api_key="ash_your_key_here")

# Get daily market data
df = client.market_daily(ts_code="000001.SZ", start_date="2024-01-01", limit=10)
print(df)

# Get northbound capital flows
flows = client.northbound_flows(start_date="2024-01-01", end_date="2024-01-31")
print(flows)

# Get financial indicators
financials = client.financial_indicators(ts_code="000001.SZ", limit=4)
print(financials)
```

## Available Methods

| Method | Endpoint | Description |
|--------|----------|-------------|
| `market_daily()` | `/v1/market/daily` | Daily OHLCV prices |
| `fundamentals()` | `/v1/market/fundamentals` | PE, PB, turnover, market cap |
| `northbound_flows()` | `/v1/flows/northbound` | Stock Connect capital flows |
| `chip_distribution()` | `/v1/chips/distribution` | Cost distribution & winner rates |
| `fx_daily()` | `/v1/fx/daily` | FX rates (default USD/CNH) |
| `index_daily()` | `/v1/indices/daily` | Index OHLCV data |
| `financial_indicators()` | `/v1/financials/indicators` | Quarterly financial metrics |

## Authentication

Get your free API key at [asharehub.com/console/register](https://asharehub.com/console/register).

## Documentation

- API Documentation: https://asharehub.com/docs
- Website: https://asharehub.com

## Requirements

- Python 3.10+
- httpx >= 0.27.0
- pydantic >= 2.0.0

## License

MIT
