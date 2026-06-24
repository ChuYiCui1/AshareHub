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
        df = client.market_daily(symbol="000001.SZ", start_date="2024-01-01")

    The instrument-code param is ``symbol`` (suffixed, e.g. ``000001.SZ``).
    With ``version="v2"`` every call hits the /v2 API (which speaks ``symbol``
    and returns JSON numbers); ``version="v1"`` (default) hits the legacy /v1 API.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        version: str = "v2",
    ):
        """``version="v2"`` switches every call to the unified-symbol /v2 API:
        bare codes (``000001``) are accepted, responses return a bare ``symbol``
        plus ``exchange`` instead of ``ts_code``, and an invalid code raises 422.
        Method signatures are unchanged — ``ts_code=``/``index_code=`` are
        transparently sent as the v2 ``symbol`` param.
        """
        if version not in ("v1", "v2"):
            raise ValueError("version must be 'v1' or 'v2'")
        self._version = version
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
        "trade_time", "updated_at",
        "publish_time", "content_cn", "tags", "url", "source",
        "symbol", "name", "area", "industry", "fullname", "enname",
        "cnspell", "market", "exchange", "curr_type", "list_status",
        "is_hs", "report_type", "comp_type", "update_flag",
        "holder_name", "holder_type", "in_de",
        "buyer", "seller", "div_proc", "type",
        "summary", "change_reason", "perf_summary",
        "con_code", "con_name", "index_code",
        "con_symbol", "con_exchange",
        "leading", "leading_code", "idx_type", "level",
        "up_stat", "limit",
        "l1_code", "l1_name", "l2_code", "l2_name",
        "l3_code", "l3_name",
    }

    # v2 unifies instrument-code params under `symbol` / `con_symbol`.
    _V2_PARAM_RENAME = {"ts_code": "symbol", "index_code": "symbol", "con_code": "con_symbol"}

    def _get(self, path: str, params: dict) -> pd.DataFrame:
        params = {k: v for k, v in params.items() if v is not None}
        if self._version == "v2":
            if path.startswith("/v1/"):
                path = "/v2/" + path[len("/v1/"):]
            params = {self._V2_PARAM_RENAME.get(k, k): v for k, v in params.items()}
        r = self._client.get(path, params=params)
        r.raise_for_status()
        data = r.json()
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        for col in df.columns:
            if col in self._STR_COLS:
                continue
            coerced = pd.to_numeric(df[col], errors="coerce")
            # Safe coercion: if to_numeric turned any real (non-null) value into NaN,
            # this column is actually text (seat names, reasons, ratings, titles, ...) —
            # keep it as-is rather than nuking it to NaN. (exalter & co. used to break here.)
            if (coerced.isna() & df[col].notna()).any():
                continue
            df[col] = coerced
        return df

    # ── Market ────────────────────────────────────────────────────────────

    def market_daily(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily OHLC price data."""
        return self._get("/v1/market/daily", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    def fundamentals(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily valuation metrics (PE, PB, turnover rate, market cap)."""
        return self._get("/v1/market/fundamentals", {
            "ts_code": symbol, "start_date": start_date,
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
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get chip distribution (cost basis) data."""
        return self._get("/v1/chips/distribution", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── FX ────────────────────────────────────────────────────────────────

    def fx_daily(
        self,
        symbol: Optional[str] = "USDCNH.FXCM",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily FX rates (default: USD/CNH)."""
        return self._get("/v1/fx/daily", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Indices ───────────────────────────────────────────────────────────

    def index_daily(
        self,
        symbol: Optional[str] = "000001.SH",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily index data (default: SSE Composite)."""
        return self._get("/v1/indices/daily", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Financials ────────────────────────────────────────────────────────

    def financial_indicators(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get financial indicators by reporting period."""
        return self._get("/v1/financials/indicators", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Money Flow ─────────────────────────────────────────────────────────

    def moneyflow(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get individual stock money flow by order size."""
        return self._get("/v1/flows/moneyflow", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Northbound Holdings ────────────────────────────────────────────────

    def northbound_holdings(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get northbound investor holdings per stock."""
        return self._get("/v1/flows/northbound-holdings", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Margin ─────────────────────────────────────────────────────────────

    def margin(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get margin trading detail (融资融券)."""
        return self._get("/v1/market/margin", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Block Trade ────────────────────────────────────────────────────────

    def block_trade(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get block trade (大宗交易) data."""
        return self._get("/v1/market/block-trade", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Top List ───────────────────────────────────────────────────────────

    def top_list(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get Dragon & Tiger list (龙虎榜) data."""
        return self._get("/v1/market/top-list", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Shareholders ───────────────────────────────────────────────────────

    def shareholders(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get shareholder count (股东户数)."""
        return self._get("/v1/market/shareholders", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Holder Trade ───────────────────────────────────────────────────────

    def holder_trade(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get major shareholder trades (股东增减持)."""
        return self._get("/v1/market/holder-trade", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Concepts ───────────────────────────────────────────────────────────

    def concepts(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get concept/theme sector indices (概念板块)."""
        return self._get("/v1/market/concepts", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Concept Members ────────────────────────────────────────────────────

    def concept_members(
        self,
        symbol: Optional[str] = None,
        con_symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get constituent stocks of a concept/theme index."""
        return self._get("/v1/market/concept-members", {
            "ts_code": symbol,
            "con_code": con_symbol,
            "start_date": start_date, "end_date": end_date,
            "limit": limit, "offset": offset,
        })

    # ── Reference ──────────────────────────────────────────────────────────

    def stock_list(
        self,
        symbol: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get A-share stock list with basic info."""
        return self._get("/v1/reference/stocks", {
            "ts_code": symbol, "limit": limit, "offset": offset,
        })

    def industry_list(
        self,
        symbol: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get Shenwan industry classification."""
        return self._get("/v1/reference/industries", {
            "ts_code": symbol, "limit": limit, "offset": offset,
        })

    # ── Adjustment Factor ─────────────────────────────────────────────────

    def adj_factor(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily adjustment factor for forward/backward price restoration."""
        return self._get("/v1/market/adj-factor", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Technical Factors ─────────────────────────────────────────────────

    def technical_factors(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get technical indicators (MACD, KDJ, RSI, BOLL, CCI) and adjusted prices."""
        return self._get("/v1/market/technical-factors", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Limit List ────────────────────────────────────────────────────────

    def limit_list(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get daily limit-up/limit-down stocks (涨跌停)."""
        return self._get("/v1/market/limit-list", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit_type": limit_type,
            "limit": limit, "offset": offset,
        })

    # ── Income Statement ──────────────────────────────────────────────────

    def income(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get income statement data."""
        return self._get("/v1/financials/income", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Balance Sheet ─────────────────────────────────────────────────────

    def balance_sheet(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get balance sheet data."""
        return self._get("/v1/financials/balance-sheet", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Cash Flow ─────────────────────────────────────────────────────────

    def cash_flow(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get cash flow statement data."""
        return self._get("/v1/financials/cash-flow", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Forecast ──────────────────────────────────────────────────────────

    def forecast(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get earnings forecast (业绩预告) data."""
        return self._get("/v1/financials/forecast", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Express ───────────────────────────────────────────────────────────

    def express(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get earnings express (业绩快报) data."""
        return self._get("/v1/financials/express", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Dividend ──────────────────────────────────────────────────────────

    def dividend(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get dividend and bonus share distribution data."""
        return self._get("/v1/shareholders/dividend", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Index Weight ──────────────────────────────────────────────────────

    def index_weight(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get index constituent stock weights."""
        return self._get("/v1/indices/index-weight", {
            "index_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Technical Factors Pro ─────────────────────────────────────────────

    def technical_factors_pro(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get professional technical factors (200+ indicators with bfq/qfq/hfq variants)."""
        return self._get("/v1/market/technical-factors-pro", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Analyst Reports ───────────────────────────────────────────────────

    def analyst_reports(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get sell-side analyst earnings forecasts and ratings."""
        return self._get("/v1/financials/analyst-reports", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Top Inst ──────────────────────────────────────────────────────────

    def top_inst(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get Dragon & Tiger list institutional seat detail."""
        return self._get("/v1/market/top-inst", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Southbound Holdings ───────────────────────────────────────────────

    def southbound_holdings(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get mainland investor holdings of HK stocks (southbound, 港股通持股)."""
        return self._get("/v1/flows/southbound-holdings", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Audit ─────────────────────────────────────────────────────────────

    def audit(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get annual audit opinions (审计意见)."""
        return self._get("/v1/financials/audit", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Main Business ─────────────────────────────────────────────────────

    def main_business(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get main business composition by segment (主营业务构成)."""
        return self._get("/v1/financials/main-business", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })

    # ── Disclosure Date ───────────────────────────────────────────────────

    def disclosure_date(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get planned/actual financial disclosure dates."""
        return self._get("/v1/financials/disclosure-date", {
            "ts_code": symbol, "start_date": start_date,
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

    # ── Real-time Quote ───────────────────────────────────────────────────

    def realtime(
        self,
        symbol: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get the real-time intraday quote snapshot (latest price per security).

        ``symbol`` may be a single code or a comma-separated basket of up to 200,
        e.g. ``"600519.SH,000001.SZ"``. Omit it to page through the whole market.
        Includes price, OHLC, previous close, pct_chg, cumulative volume/turnover
        and the source quote timestamp. Continuously refreshed during trading hours.
        """
        return self._get("/v1/market/realtime", {
            "ts_code": symbol, "limit": limit, "offset": offset,
        })

    # ── News Flash ────────────────────────────────────────────────────────

    def news_flash(
        self,
        source: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        importance: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> pd.DataFrame:
        """Get real-time Chinese financial news flashes (财经快讯).

        ``source`` is required — one feed per call: "cls" (财联社), "jin10" (金十),
        or "sina" (新浪). Content is Chinese (content_cn). Ordered newest first.
        Optional: importance (>= filter), start_date/end_date (YYYY-MM-DD on publish_time).
        """
        return self._get("/v1/news/flash", {
            "source": source, "start_date": start_date, "end_date": end_date,
            "importance": importance, "limit": limit, "offset": offset,
        })
