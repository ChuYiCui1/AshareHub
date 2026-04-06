"""AShareHub Python SDK — typed client for Chinese A-Share market data."""

from typing import Optional

import httpx
import pandas as pd

DEFAULT_BASE_URL = "https://asharehub.com"


class AShareHub:
    """Client for the AShareHub API.

    Usage::

        from asharehub import AShareHub

        client = AShareHub(api_key="ash_...")
        df = client.market_daily(ts_code="000001.SZ", start_date="2024-01-01")
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

    # 已知的字符串列，不做数值转换
    _STR_COLS = {
        "ts_code", "trade_date", "end_date", "ann_date", "f_ann_date",
        "report_date", "cal_date", "pretrade_date", "record_date",
        "ex_date", "pay_date", "div_listdate", "imp_ann_date",
        "list_date", "delist_date", "begin_date", "close_date",
        "first_ann_date", "first_time", "last_time",
        "symbol", "name", "area", "industry", "fullname", "enname",
        "cnspell", "market", "exchange", "curr_type", "list_status",
        "is_hs", "report_type", "comp_type", "update_flag",
        "holder_name", "holder_type", "in_de",
        "buyer", "seller", "div_proc", "type",
        "summary", "change_reason", "perf_summary",
        "con_code", "con_name", "index_code",
        "leading", "leading_code", "idx_type", "level",
        "up_stat", "limit",
        "l1_code", "l1_name", "l2_code", "l2_name",
        "l3_code", "l3_name",
    }

    def _get(self, path: str, params: dict) -> pd.DataFrame:
        params = {k: v for k, v in params.items() if v is not None}
        r = self._client.get(path, params=params)
        r.raise_for_status()
        data = r.json()
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        for col in df.columns:
            if col not in self._STR_COLS:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    # ── Market ────────────────────────────────────────────────────────────

    def market_daily(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily OHLC price data."""
        return self._get("/v1/market/daily", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    def fundamentals(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily valuation metrics (PE, PB, turnover rate, market cap)."""
        return self._get("/v1/market/fundamentals", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Flows ─────────────────────────────────────────────────────────────

    def moneyflow_hsgt(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get Stock Connect capital flows (HSGT, northbound + southbound)."""
        return self._get("/v1/flows/moneyflow-hsgt", {
            "start_date": start_date, "end_date": end_date,
            "limit": limit, "offset": offset,
        })

    # ── Chips ─────────────────────────────────────────────────────────────

    def chip_distribution(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get chip distribution (cost basis) data."""
        return self._get("/v1/chips/distribution", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── FX ────────────────────────────────────────────────────────────────

    def fx_daily(
        self,
        ts_code: Optional[str] = "USDCNH.FXCM",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily FX rates (default: USD/CNH)."""
        return self._get("/v1/fx/daily", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Indices ───────────────────────────────────────────────────────────

    def index_daily(
        self,
        ts_code: Optional[str] = "000001.SH",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily index data (default: SSE Composite)."""
        return self._get("/v1/indices/daily", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Financials ────────────────────────────────────────────────────────

    def financial_indicators(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get financial indicators by reporting period."""
        return self._get("/v1/financials/indicators", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Money Flow ─────────────────────────────────────────────────────────

    def moneyflow(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get individual stock money flow by order size."""
        return self._get("/v1/flows/moneyflow", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Northbound Holdings ────────────────────────────────────────────────

    def northbound_holdings(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get northbound investor holdings per stock."""
        return self._get("/v1/flows/northbound-holdings", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Margin ─────────────────────────────────────────────────────────────

    def margin(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get margin trading detail (融资融券)."""
        return self._get("/v1/market/margin", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Block Trade ────────────────────────────────────────────────────────

    def block_trade(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get block trade (大宗交易) data."""
        return self._get("/v1/market/block-trade", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Top List ───────────────────────────────────────────────────────────

    def top_list(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get Dragon & Tiger list (龙虎榜) data."""
        return self._get("/v1/market/top-list", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Shareholders ───────────────────────────────────────────────────────

    def shareholders(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get shareholder count (股东户数)."""
        return self._get("/v1/market/shareholders", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Holder Trade ───────────────────────────────────────────────────────

    def holder_trade(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get major shareholder trades (股东增减持)."""
        return self._get("/v1/market/holder-trade", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Concepts ───────────────────────────────────────────────────────────

    def concepts(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get concept/theme sector indices (概念板块)."""
        return self._get("/v1/market/concepts", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Concept Members ────────────────────────────────────────────────────

    def concept_members(
        self,
        ts_code: Optional[str] = None,
        con_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get constituent stocks of a concept/theme index."""
        return self._get("/v1/market/concept-members", {
            "ts_code": ts_code, "con_code": con_code,
            "start_date": start_date, "end_date": end_date,
            "limit": limit, "offset": offset,
        })

    # ── Reference ──────────────────────────────────────────────────────────

    def stock_list(
        self,
        ts_code: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get A-share stock list with basic info."""
        return self._get("/v1/reference/stocks", {
            "ts_code": ts_code, "limit": limit, "offset": offset,
        })

    def industry_list(
        self,
        ts_code: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get Shenwan industry classification."""
        return self._get("/v1/reference/industries", {
            "ts_code": ts_code, "limit": limit, "offset": offset,
        })

    # ── Adjustment Factor ─────────────────────────────────────────────────

    def adj_factor(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily adjustment factor for forward/backward price restoration."""
        return self._get("/v1/market/adj-factor", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Technical Factors ─────────────────────────────────────────────────

    def technical_factors(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get technical indicators (MACD, KDJ, RSI, BOLL, CCI) and adjusted prices."""
        return self._get("/v1/market/technical-factors", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Limit List ────────────────────────────────────────────────────────

    def limit_list(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily limit-up/limit-down stocks (涨跌停)."""
        return self._get("/v1/market/limit-list", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit_type": limit_type,
            "limit": limit, "offset": offset,
        })

    # ── Income Statement ──────────────────────────────────────────────────

    def income(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get income statement data."""
        return self._get("/v1/financials/income", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Balance Sheet ─────────────────────────────────────────────────────

    def balance_sheet(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get balance sheet data."""
        return self._get("/v1/financials/balance-sheet", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Cash Flow ─────────────────────────────────────────────────────────

    def cash_flow(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get cash flow statement data."""
        return self._get("/v1/financials/cash-flow", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Forecast ──────────────────────────────────────────────────────────

    def forecast(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get earnings forecast (业绩预告) data."""
        return self._get("/v1/financials/forecast", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Express ───────────────────────────────────────────────────────────

    def express(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get earnings express (业绩快报) data."""
        return self._get("/v1/financials/express", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Dividend ──────────────────────────────────────────────────────────

    def dividend(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get dividend and bonus share distribution data."""
        return self._get("/v1/shareholders/dividend", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Index Weight ──────────────────────────────────────────────────────

    def index_weight(
        self,
        index_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get index constituent stock weights."""
        return self._get("/v1/indices/index-weight", {
            "index_code": index_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Trade Calendar ────────────────────────────────────────────────────

    def trade_calendar(
        self,
        exchange: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        is_open: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get trading calendar for SSE/SZSE."""
        return self._get("/v1/reference/trade-calendar", {
            "exchange": exchange, "start_date": start_date,
            "end_date": end_date, "is_open": is_open,
            "limit": limit, "offset": offset,
        })
