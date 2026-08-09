"""Pydantic models generated from the AShareHub V2 public field contract.

The SDK returns :class:`pandas.DataFrame` objects, so these models are provided
for schema discovery and validation rather than as method return values.  Field
names come directly from ``public_contract.json``; internal V1/RDS names such
as ``ts_code`` and ``con_code`` are intentionally absent.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, create_model

from asharehub.contract import PUBLIC_CONTRACT


_MODEL_NAMES = {
    "market_daily": "DailyBar",
    "fundamentals": "Fundamentals",
    "moneyflow_hsgt": "MoneyflowHsgt",
    "chip_distribution": "ChipDistribution",
    "fx_daily": "FxDaily",
    "index_daily": "IndexDaily",
    "etf_basic": "ETFBasic",
    "etf_indices": "ETFIndex",
    "etf_daily": "ETFDaily",
    "etf_adj_factor": "ETFAdjustmentFactor",
    "etf_share_size": "ETFShareSize",
    "etf_nav": "ETFNav",
    "etf_portfolio": "ETFPortfolio",
    "etf_sh_basket": "ETFShanghaiBasket",
    "etf_sz_basket": "ETFShenzhenBasket",
    "hk_stock_list": "HKStockBasic",
    "hk_daily": "HKDailyBar",
    "hk_trade_calendar": "HKTradeCalendar",
    "financial_indicators": "FinaIndicator",
    "moneyflow": "MoneyFlow",
    "northbound_holdings": "NorthboundHolding",
    "margin": "MarginDetail",
    "block_trade": "BlockTrade",
    "top_list": "TopList",
    "shareholders": "ShareholderNumber",
    "holder_trade": "HolderTrade",
    "concepts": "ConceptIndex",
    "concept_members": "ConceptMember",
    "stock_list": "StockBasic",
    "industry_list": "IndustryClassification",
    "adj_factor": "AdjFactor",
    "technical_factors": "StkFactor",
    "limit_list": "LimitList",
    "income": "IncomeStatement",
    "balance_sheet": "BalanceSheet",
    "cash_flow": "CashFlow",
    "forecast": "Forecast",
    "express": "Express",
    "dividend": "Dividend",
    "index_weight": "IndexWeight",
    "technical_factors_pro": "TechnicalFactorsPro",
    "analyst_reports": "AnalystReport",
    "top_inst": "TopInst",
    "southbound_holdings": "SouthboundHolding",
    "audit": "Audit",
    "main_business": "MainBusiness",
    "disclosure_date": "DisclosureDate",
    "trade_calendar": "TradeCalendar",
    "realtime": "RealtimeQuote",
    "news_flash": "NewsFlash",
}


def _make_model(method: str, name: str) -> type[BaseModel]:
    fields = PUBLIC_CONTRACT["interfaces"][method]["response_fields"]
    return create_model(
        name,
        **{field: (Any | None, None) for field in fields},
    )


MODEL_BY_METHOD = {
    method: _make_model(method, name)
    for method, name in _MODEL_NAMES.items()
}
globals().update({model.__name__: model for model in MODEL_BY_METHOD.values()})


__all__ = ["MODEL_BY_METHOD", *_MODEL_NAMES.values()]
