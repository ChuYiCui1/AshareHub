"""AShareHub Python SDK — typed client for Chinese A-Share market data."""

from typing import Optional

import httpx

from asharehub.models import (
    DailyBar,
    Fundamentals,
    NorthboundFlow,
    ChipDistribution,
    FxDaily,
    IndexDaily,
    FinaIndicator,
)

DEFAULT_BASE_URL = "https://api.asharehub.com"


class AShareHub:
    """Client for the AShareHub API.

    Usage::

        from asharehub import AShareHub

        client = AShareHub(api_key="ash_...")
        bars = client.daily("000001.SZ", start_date="2024-01-01")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self._client = httpx.Client(
            base_url=base_url,
            headers={"X-API-Key": api_key},
            timeout=timeout,
        )

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _get(self, path: str, params: dict) -> list[dict]:
        params = {k: v for k, v in params.items() if v is not None}
        r = self._client.get(path, params=params)
        r.raise_for_status()
        return r.json()

    # ── Market ────────────────────────────────────────────────────────────

    def daily(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[DailyBar]:
        """Get daily OHLC price data."""
        data = self._get("/v1/market/daily", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [DailyBar(**row) for row in data]

    def fundamentals(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Fundamentals]:
        """Get daily valuation metrics (PE, PB, turnover rate, market cap)."""
        data = self._get("/v1/market/fundamentals", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [Fundamentals(**row) for row in data]

    # ── Flows ─────────────────────────────────────────────────────────────

    def northbound(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[NorthboundFlow]:
        """Get northbound capital flows (Stock Connect)."""
        data = self._get("/v1/flows/northbound", {
            "start_date": start_date, "end_date": end_date,
            "limit": limit, "offset": offset,
        })
        return [NorthboundFlow(**row) for row in data]

    # ── Chips ─────────────────────────────────────────────────────────────

    def chips(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ChipDistribution]:
        """Get chip distribution (cost basis) data."""
        data = self._get("/v1/chips/distribution", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [ChipDistribution(**row) for row in data]

    # ── FX ────────────────────────────────────────────────────────────────

    def fx(
        self,
        ts_code: Optional[str] = "USDCNH.FXCM",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[FxDaily]:
        """Get daily FX rates (default: USD/CNH)."""
        data = self._get("/v1/fx/daily", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [FxDaily(**row) for row in data]

    # ── Indices ───────────────────────────────────────────────────────────

    def indices(
        self,
        ts_code: Optional[str] = "000001.SH",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[IndexDaily]:
        """Get daily index data (default: SSE Composite)."""
        data = self._get("/v1/indices/daily", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [IndexDaily(**row) for row in data]

    # ── Financials ────────────────────────────────────────────────────────

    def financials(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[FinaIndicator]:
        """Get financial indicators by reporting period."""
        data = self._get("/v1/financials/indicators", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [FinaIndicator(**row) for row in data]
