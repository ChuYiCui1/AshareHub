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
    MoneyFlow,
    NorthboundHolding,
    MarginDetail,
    BlockTrade,
    TopList,
    ShareholderNumber,
    HolderTrade,
    ConceptIndex,
    ConceptMember,
    StockBasic,
    IndustryClassification,
    AdjFactor,
    StkFactor,
    LimitList,
    IncomeStatement,
    BalanceSheet,
    CashFlow,
    Forecast,
    Express,
    Dividend,
    IndexWeight,
    TradeCalendar,
)

DEFAULT_BASE_URL = "https://asharehub.com"


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

    def market_daily(
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

    def northbound_flows(
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

    def chip_distribution(
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

    def fx_daily(
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

    def index_daily(
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

    def financial_indicators(
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

    # ── Money Flow ─────────────────────────────────────────────────────────

    def moneyflow(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MoneyFlow]:
        """Get individual stock money flow by order size."""
        data = self._get("/v1/flows/moneyflow", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [MoneyFlow(**row) for row in data]

    # ── Northbound Holdings ────────────────────────────────────────────────

    def northbound_holdings(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[NorthboundHolding]:
        """Get northbound investor holdings per stock."""
        data = self._get("/v1/flows/northbound-holdings", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [NorthboundHolding(**row) for row in data]

    # ── Margin ─────────────────────────────────────────────────────────────

    def margin(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MarginDetail]:
        """Get margin trading detail (融资融券)."""
        data = self._get("/v1/market/margin", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [MarginDetail(**row) for row in data]

    # ── Block Trade ────────────────────────────────────────────────────────

    def block_trade(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[BlockTrade]:
        """Get block trade (大宗交易) data."""
        data = self._get("/v1/market/block-trade", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [BlockTrade(**row) for row in data]

    # ── Top List ───────────────────────────────────────────────────────────

    def top_list(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TopList]:
        """Get Dragon & Tiger list (龙虎榜) data."""
        data = self._get("/v1/market/top-list", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [TopList(**row) for row in data]

    # ── Shareholders ───────────────────────────────────────────────────────

    def shareholders(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ShareholderNumber]:
        """Get shareholder count (股东户数)."""
        data = self._get("/v1/market/shareholders", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [ShareholderNumber(**row) for row in data]

    # ── Holder Trade ───────────────────────────────────────────────────────

    def holder_trade(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[HolderTrade]:
        """Get major shareholder trades (股东增减持)."""
        data = self._get("/v1/market/holder-trade", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [HolderTrade(**row) for row in data]

    # ── Concepts ───────────────────────────────────────────────────────────

    def concepts(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ConceptIndex]:
        """Get concept/theme sector indices (概念板块)."""
        data = self._get("/v1/market/concepts", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [ConceptIndex(**row) for row in data]

    # ── Concept Members ────────────────────────────────────────────────────

    def concept_members(
        self,
        ts_code: Optional[str] = None,
        con_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ConceptMember]:
        """Get constituent stocks of a concept/theme index."""
        data = self._get("/v1/market/concept-members", {
            "ts_code": ts_code, "con_code": con_code,
            "start_date": start_date, "end_date": end_date,
            "limit": limit, "offset": offset,
        })
        return [ConceptMember(**row) for row in data]

    # ── Reference ──────────────────────────────────────────────────────────

    def stock_list(
        self,
        ts_code: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[StockBasic]:
        """Get A-share stock list with basic info."""
        data = self._get("/v1/reference/stocks", {
            "ts_code": ts_code, "limit": limit, "offset": offset,
        })
        return [StockBasic(**row) for row in data]

    def industry_list(
        self,
        ts_code: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[IndustryClassification]:
        """Get Shenwan industry classification."""
        data = self._get("/v1/reference/industries", {
            "ts_code": ts_code, "limit": limit, "offset": offset,
        })
        return [IndustryClassification(**row) for row in data]

    # ── Adjustment Factor ─────────────────────────────────────────────────

    def adj_factor(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AdjFactor]:
        """Get daily adjustment factor for forward/backward price restoration."""
        data = self._get("/v1/market/adj-factor", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [AdjFactor(**row) for row in data]

    # ── Technical Factors ─────────────────────────────────────────────────

    def technical_factors(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[StkFactor]:
        """Get technical indicators (MACD, KDJ, RSI, BOLL, CCI) and adjusted prices."""
        data = self._get("/v1/market/technical-factors", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [StkFactor(**row) for row in data]

    # ── Limit List ────────────────────────────────────────────────────────

    def limit_list(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[LimitList]:
        """Get daily limit-up/limit-down stocks (涨跌停)."""
        data = self._get("/v1/market/limit-list", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit_type": limit_type,
            "limit": limit, "offset": offset,
        })
        return [LimitList(**row) for row in data]

    # ── Income Statement ──────────────────────────────────────────────────

    def income(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[IncomeStatement]:
        """Get income statement data."""
        data = self._get("/v1/financials/income", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [IncomeStatement(**row) for row in data]

    # ── Balance Sheet ─────────────────────────────────────────────────────

    def balance_sheet(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[BalanceSheet]:
        """Get balance sheet data."""
        data = self._get("/v1/financials/balance-sheet", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [BalanceSheet(**row) for row in data]

    # ── Cash Flow ─────────────────────────────────────────────────────────

    def cash_flow(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[CashFlow]:
        """Get cash flow statement data."""
        data = self._get("/v1/financials/cash-flow", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [CashFlow(**row) for row in data]

    # ── Forecast ──────────────────────────────────────────────────────────

    def forecast(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Forecast]:
        """Get earnings forecast (业绩预告) data."""
        data = self._get("/v1/financials/forecast", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [Forecast(**row) for row in data]

    # ── Express ───────────────────────────────────────────────────────────

    def express(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Express]:
        """Get earnings express (业绩快报) data."""
        data = self._get("/v1/financials/express", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [Express(**row) for row in data]

    # ── Dividend ──────────────────────────────────────────────────────────

    def dividend(
        self,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Dividend]:
        """Get dividend and bonus share distribution data."""
        data = self._get("/v1/shareholders/dividend", {
            "ts_code": ts_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [Dividend(**row) for row in data]

    # ── Index Weight ──────────────────────────────────────────────────────

    def index_weight(
        self,
        index_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[IndexWeight]:
        """Get index constituent stock weights."""
        data = self._get("/v1/indices/index-weight", {
            "index_code": index_code, "start_date": start_date,
            "end_date": end_date, "limit": limit, "offset": offset,
        })
        return [IndexWeight(**row) for row in data]

    # ── Trade Calendar ────────────────────────────────────────────────────

    def trade_calendar(
        self,
        exchange: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        is_open: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TradeCalendar]:
        """Get trading calendar for SSE/SZSE."""
        data = self._get("/v1/reference/trade-calendar", {
            "exchange": exchange, "start_date": start_date,
            "end_date": end_date, "is_open": is_open,
            "limit": limit, "offset": offset,
        })
        return [TradeCalendar(**row) for row in data]
