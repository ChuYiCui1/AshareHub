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
        df = client.market_daily(symbol="000001.SZ", start_date="20240101")

    The instrument-code param is ``symbol`` (suffixed, e.g. ``000001.SZ``).
    By default the client targets the **/v2** API; pass ``version="v1"`` for the
    legacy API.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        version: str = "v2",
    ):
        """``version`` selects the API surface (default ``"v2"``):

        - ``"v2"`` — unified-symbol API: responses use ``symbol`` (the suffixed
          code, e.g. ``000001.SZ``) and real JSON numbers. An unparseable code
          returns HTTP 422.
        - ``"v1"`` — legacy Tushare-style API: responses use ``ts_code`` and
          DECIMAL strings.

        Either way the method param is ``symbol``.
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
        "cnspell", "cn_spell", "market", "exchange", "curr_type", "list_status",
        "isin",
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
        "nav_date", "setup_date", "base_date", "pub_date",
        "csname", "extname", "cname", "index_name", "index_symbol",
        "mgr_name", "custod_name", "etf_type", "etf_name",
        "indx_name", "indx_csname", "pub_party_name", "adj_circle",
        "sub_flag",
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
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get daily OHLC price data. Filter: trade_date."""
        return self._get("/v1/market/daily", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    def fundamentals(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get daily valuation metrics (PE, PB, turnover rate, market cap). Filter: trade_date."""
        return self._get("/v1/market/fundamentals", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Flows ─────────────────────────────────────────────────────────────

    def moneyflow_hsgt(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get Stock Connect capital flows (HSGT, northbound + southbound). Filter: trade_date."""
        return self._get("/v1/flows/moneyflow-hsgt", {
            "start_date": start_date, "end_date": end_date,
            "trade_date": trade_date,
        })

    # ── Chips ─────────────────────────────────────────────────────────────

    def chip_distribution(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get chip distribution (cost basis) data. Filter: trade_date."""
        return self._get("/v1/chips/distribution", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── FX ────────────────────────────────────────────────────────────────

    def fx_daily(
        self,
        symbol: Optional[str] = "USDCNH.FXCM",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get daily FX rates (default: USD/CNH). Filter: trade_date."""
        return self._get("/v1/fx/daily", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Indices ───────────────────────────────────────────────────────────

    def index_daily(
        self,
        symbol: Optional[str] = "000001.SH",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get daily index data (default: SSE Composite). Filter: trade_date."""
        return self._get("/v1/indices/daily", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── ETF ──────────────────────────────────────────────────────────────

    def etf_basic(
        self,
        symbol: Optional[str] = None,
        index_symbol: Optional[str] = None,
        list_status: Optional[str] = None,
        exchange: Optional[str] = None,
        manager: Optional[str] = None,
        etf_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get the domestic ETF directory, including QDII ETFs."""
        return self._get("/v1/etf/basic", {
            "ts_code": symbol, "index_symbol": index_symbol,
            "list_status": list_status, "exchange": exchange,
            "manager": manager, "etf_type": etf_type,
        })

    def etf_indices(
        self,
        symbol: Optional[str] = None,
        pub_date: Optional[str] = None,
        base_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get benchmark indices tracked by domestic ETFs."""
        return self._get("/v1/etf/indices", {
            "ts_code": symbol, "pub_date": pub_date, "base_date": base_date,
        })

    def etf_daily(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get ETF daily OHLC, volume and turnover."""
        return self._get("/v1/etf/daily", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    def etf_adj_factor(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get ETF adjustment factors."""
        return self._get("/v1/etf/adj-factor", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    def etf_share_size(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get daily ETF shares, assets, NAV and close."""
        return self._get("/v1/etf/share-size", {
            "ts_code": symbol, "start_date": start_date, "end_date": end_date,
            "trade_date": trade_date, "exchange": exchange,
        })

    def etf_nav(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        nav_date: Optional[str] = None,
        ann_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get ETF unit, accumulated and adjusted NAV."""
        return self._get("/v1/etf/nav", {
            "ts_code": symbol, "start_date": start_date, "end_date": end_date,
            "nav_date": nav_date, "ann_date": ann_date,
        })

    def etf_portfolio(
        self,
        symbol: Optional[str] = None,
        con_symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get an ETF's periodically disclosed security holdings."""
        return self._get("/v1/etf/portfolio", {
            "ts_code": symbol, "con_code": con_symbol,
            "start_date": start_date, "end_date": end_date,
            "period": period, "ann_date": ann_date,
        })

    def etf_sh_basket(
        self,
        symbol: Optional[str] = None,
        con_symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get the Shanghai ETF creation/redemption PCF basket."""
        return self._get("/v1/etf/basket/sh", {
            "ts_code": symbol, "con_code": con_symbol,
            "start_date": start_date, "end_date": end_date,
            "trade_date": trade_date, "exchange": exchange,
        })

    def etf_sz_basket(
        self,
        symbol: Optional[str] = None,
        con_symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get the Shenzhen ETF creation/redemption PCF basket."""
        return self._get("/v1/etf/basket/sz", {
            "ts_code": symbol, "con_code": con_symbol,
            "start_date": start_date, "end_date": end_date,
            "trade_date": trade_date, "exchange": exchange,
        })

    # ── Hong Kong Equities ───────────────────────────────────────────────

    def hk_stock_list(
        self,
        symbol: Optional[str] = None,
        list_status: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get the Hong Kong stock directory.

        Symbols use Tushare's five-digit suffixed form, e.g. ``00700.HK``.
        """
        return self._get("/v1/hk/basic", {
            "ts_code": symbol,
            "list_status": list_status,
        })

    def hk_daily(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get unadjusted Hong Kong daily OHLCV bars.

        Prices and turnover are in HKD; volume is in shares.  This endpoint does
        not currently expose Hong Kong adjustment factors.
        """
        return self._get("/v1/hk/daily", {
            "ts_code": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "trade_date": trade_date,
        })

    def hk_trade_calendar(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        is_open: Optional[int] = None,
    ) -> pd.DataFrame:
        """Get the Hong Kong Exchange trading calendar."""
        return self._get("/v1/hk/trade-calendar", {
            "start_date": start_date,
            "end_date": end_date,
            "is_open": is_open,
        })

    # ── Financials ────────────────────────────────────────────────────────

    def financial_indicators(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get financial indicators by reporting period. Filters: period, ann_date."""
        return self._get("/v1/financials/indicators", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period, "ann_date": ann_date,
        })

    # ── Money Flow ─────────────────────────────────────────────────────────

    def moneyflow(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get individual stock money flow by order size. Filter: trade_date."""
        return self._get("/v1/flows/moneyflow", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Northbound Holdings ────────────────────────────────────────────────

    def northbound_holdings(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get northbound investor holdings per stock. Filter: trade_date."""
        return self._get("/v1/flows/northbound-holdings", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Margin ─────────────────────────────────────────────────────────────

    def margin(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get margin trading detail (融资融券). Filter: trade_date."""
        return self._get("/v1/market/margin", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Block Trade ────────────────────────────────────────────────────────

    def block_trade(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get block trade (大宗交易) data. Filter: trade_date."""
        return self._get("/v1/market/block-trade", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Top List ───────────────────────────────────────────────────────────

    def top_list(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get Dragon & Tiger list (龙虎榜) data. Filter: trade_date."""
        return self._get("/v1/market/top-list", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Shareholders ───────────────────────────────────────────────────────

    def shareholders(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        enddate: Optional[str] = None,
        ann_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get shareholder count (股东户数). Filters: enddate, ann_date."""
        return self._get("/v1/market/shareholders", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "enddate": enddate, "ann_date": ann_date,
        })

    # ── Holder Trade ───────────────────────────────────────────────────────

    def holder_trade(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_type: Optional[str] = None,
        holder_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get major shareholder trades (股东增减持). Filters: trade_type, holder_type."""
        return self._get("/v1/market/holder-trade", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_type": trade_type, "holder_type": holder_type,
        })

    # ── Concepts ───────────────────────────────────────────────────────────

    def concepts(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
        name: Optional[str] = None,
        idx_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get concept/theme sector indices (概念板块). Filters: trade_date, name, idx_type."""
        return self._get("/v1/market/concepts", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
            "name": name, "idx_type": idx_type,
        })

    # ── Concept Members ────────────────────────────────────────────────────

    def concept_members(
        self,
        symbol: Optional[str] = None,
        con_symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get constituent stocks of a concept/theme index. Filter: trade_date."""
        return self._get("/v1/market/concept-members", {
            "ts_code": symbol,
            "con_code": con_symbol,
            "start_date": start_date, "end_date": end_date,
            "trade_date": trade_date,
        })

    # ── Reference ──────────────────────────────────────────────────────────

    def stock_list(
        self,
        symbol: Optional[str] = None,
        name: Optional[str] = None,
        market: Optional[str] = None,
        list_status: Optional[str] = None,
        exchange: Optional[str] = None,
        is_hs: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get A-share stock list with basic info. Filters: name, market, list_status,
        exchange, is_hs. Returns the full directory (no limit/offset — not paginated)."""
        return self._get("/v1/reference/stocks", {
            "ts_code": symbol, "name": name, "market": market,
            "list_status": list_status, "exchange": exchange, "is_hs": is_hs,
        })

    def industry_list(
        self,
        symbol: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get Shenwan industry classification (full set — no limit/offset, not paginated)."""
        return self._get("/v1/reference/industries", {
            "ts_code": symbol,
        })

    # ── Adjustment Factor ─────────────────────────────────────────────────

    def adj_factor(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get daily adjustment factor for forward/backward price restoration. Filter: trade_date."""
        return self._get("/v1/market/adj-factor", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Technical Factors ─────────────────────────────────────────────────

    def technical_factors(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get technical indicators (MACD, KDJ, RSI, BOLL, CCI) and adjusted prices. Filter: trade_date."""
        return self._get("/v1/market/technical-factors", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Limit List ────────────────────────────────────────────────────────

    def limit_list(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
        limit_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get daily limit-up/limit-down stocks (涨跌停). Filter: trade_date."""
        return self._get("/v1/market/limit-list", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
            "limit_type": limit_type,
        })

    # ── Income Statement ──────────────────────────────────────────────────

    def income(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
        f_ann_date: Optional[str] = None,
        report_type: Optional[str] = None,
        comp_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get income statement data. Filters: period, ann_date, f_ann_date, report_type, comp_type."""
        return self._get("/v1/financials/income", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period, "ann_date": ann_date,
            "f_ann_date": f_ann_date, "report_type": report_type,
            "comp_type": comp_type,
        })

    # ── Balance Sheet ─────────────────────────────────────────────────────

    def balance_sheet(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
        report_type: Optional[str] = None,
        comp_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get balance sheet data. Filters: period, ann_date, report_type, comp_type."""
        return self._get("/v1/financials/balance-sheet", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period, "ann_date": ann_date,
            "report_type": report_type, "comp_type": comp_type,
        })

    # ── Cash Flow ─────────────────────────────────────────────────────────

    def cash_flow(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
        f_ann_date: Optional[str] = None,
        report_type: Optional[str] = None,
        comp_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get cash flow statement data. Filters: period, ann_date, f_ann_date, report_type, comp_type."""
        return self._get("/v1/financials/cash-flow", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period, "ann_date": ann_date,
            "f_ann_date": f_ann_date, "report_type": report_type,
            "comp_type": comp_type,
        })

    # ── Forecast ──────────────────────────────────────────────────────────

    def forecast(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get earnings forecast (业绩预告) data. Filters: period, type."""
        return self._get("/v1/financials/forecast", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period, "type": type,
        })

    # ── Express ───────────────────────────────────────────────────────────

    def express(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get earnings express (业绩快报) data. Filter: period."""
        return self._get("/v1/financials/express", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period,
        })

    # ── Dividend ──────────────────────────────────────────────────────────

    def dividend(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        record_date: Optional[str] = None,
        ex_date: Optional[str] = None,
        imp_ann_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get dividend and bonus share distribution data. Filters: record_date, ex_date, imp_ann_date."""
        return self._get("/v1/shareholders/dividend", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "record_date": record_date,
            "ex_date": ex_date, "imp_ann_date": imp_ann_date,
        })

    # ── Index Weight ──────────────────────────────────────────────────────

    def index_weight(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get index constituent stock weights. Filter: trade_date."""
        return self._get("/v1/indices/index-weight", {
            "index_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Technical Factors Pro ─────────────────────────────────────────────

    def technical_factors_pro(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get professional technical factors (200+ indicators with bfq/qfq/hfq variants). Filter: trade_date."""
        return self._get("/v1/market/technical-factors-pro", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Analyst Reports ───────────────────────────────────────────────────

    def analyst_reports(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get sell-side analyst earnings forecasts and ratings."""
        return self._get("/v1/financials/analyst-reports", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date,
        })

    # ── Top Inst ──────────────────────────────────────────────────────────

    def top_inst(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get Dragon & Tiger list institutional seat detail. Filter: trade_date."""
        return self._get("/v1/market/top-inst", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Southbound Holdings ───────────────────────────────────────────────

    def southbound_holdings(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get mainland investor holdings of HK stocks (southbound, 港股通持股). Filter: trade_date."""
        return self._get("/v1/flows/southbound-holdings", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "trade_date": trade_date,
        })

    # ── Audit ─────────────────────────────────────────────────────────────

    def audit(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get annual audit opinions (审计意见). Filters: period, ann_date."""
        return self._get("/v1/financials/audit", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period, "ann_date": ann_date,
        })

    # ── Main Business ─────────────────────────────────────────────────────

    def main_business(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get main business composition by segment (主营业务构成). Filter: period."""
        return self._get("/v1/financials/main-business", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "period": period,
        })

    # ── Disclosure Date ───────────────────────────────────────────────────

    def disclosure_date(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        pre_date: Optional[str] = None,
        actual_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get planned/actual financial disclosure dates. Filters: pre_date, actual_date."""
        return self._get("/v1/financials/disclosure-date", {
            "ts_code": symbol, "start_date": start_date,
            "end_date": end_date, "pre_date": pre_date, "actual_date": actual_date,
        })

    # ── Trade Calendar ────────────────────────────────────────────────────

    def trade_calendar(
        self,
        exchange: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        is_open: Optional[int] = None,
    ) -> pd.DataFrame:
        """Get trading calendar for SSE/SZSE."""
        return self._get("/v1/reference/trade-calendar", {
            "exchange": exchange, "start_date": start_date,
            "end_date": end_date, "is_open": is_open,
        })

    # ── Real-time Quote ───────────────────────────────────────────────────

    def realtime(
        self,
        symbol: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get the real-time intraday quote snapshot (latest price per security).

        ``symbol`` may be a single code or a comma-separated basket of up to 200,
        e.g. ``"600519.SH,000001.SZ"``. Omit it to page through the whole market.
        Includes price, OHLC, previous close, pct_chg, cumulative volume/turnover
        and the source quote timestamp. Continuously refreshed during trading hours.
        """
        return self._get("/v1/market/realtime", {
            "ts_code": symbol,
        })

    # ── News Flash ────────────────────────────────────────────────────────

    def news_flash(
        self,
        source: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        importance: Optional[int] = None,
    ) -> pd.DataFrame:
        """Get real-time Chinese financial news flashes (财经快讯).

        ``source`` is required — one feed per call: "cls" (财联社), "jin10" (金十),
        or "sina" (新浪). Content is Chinese (content_cn). Ordered newest first.
        Optional: importance (>= filter), start_date/end_date (YYYYMMDD on publish_time).
        """
        return self._get("/v1/news/flash", {
            "source": source, "start_date": start_date, "end_date": end_date,
            "importance": importance,
        })
