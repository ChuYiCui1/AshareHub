"""Pydantic models matching the AShareHub API response schemas."""

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class DailyBar(BaseModel):
    ts_code: str
    trade_date: date
    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    close: Optional[Decimal] = None
    pre_close: Optional[Decimal] = None
    change: Optional[Decimal] = None
    pct_chg: Optional[Decimal] = None
    vol: Optional[Decimal] = None
    amount: Optional[Decimal] = None


class Fundamentals(BaseModel):
    ts_code: str
    trade_date: date
    close: Optional[Decimal] = None
    turnover_rate: Optional[Decimal] = None
    turnover_rate_f: Optional[Decimal] = None
    volume_ratio: Optional[Decimal] = None
    pe: Optional[Decimal] = None
    pe_ttm: Optional[Decimal] = None
    pb: Optional[Decimal] = None
    ps: Optional[Decimal] = None
    ps_ttm: Optional[Decimal] = None
    dv_ratio: Optional[Decimal] = None
    dv_ttm: Optional[Decimal] = None
    total_share: Optional[Decimal] = None
    float_share: Optional[Decimal] = None
    free_share: Optional[Decimal] = None
    total_mv: Optional[Decimal] = None
    circ_mv: Optional[Decimal] = None


class NorthboundFlow(BaseModel):
    trade_date: date
    ggt_ss: Optional[Decimal] = None
    ggt_sz: Optional[Decimal] = None
    hgt_ss: Optional[Decimal] = None
    hgt_sz: Optional[Decimal] = None
    north_money: Optional[Decimal] = None
    south_money: Optional[Decimal] = None


class ChipDistribution(BaseModel):
    ts_code: str
    trade_date: date
    his_low: Optional[Decimal] = None
    his_high: Optional[Decimal] = None
    cost_5pct: Optional[Decimal] = None
    cost_15pct: Optional[Decimal] = None
    cost_50pct: Optional[Decimal] = None
    cost_85pct: Optional[Decimal] = None
    cost_95pct: Optional[Decimal] = None
    weight_avg: Optional[Decimal] = None
    winner_rate: Optional[Decimal] = None


class FxDaily(BaseModel):
    ts_code: str
    trade_date: date
    bid_open: Optional[Decimal] = None
    bid_close: Optional[Decimal] = None
    bid_high: Optional[Decimal] = None
    bid_low: Optional[Decimal] = None
    ask_open: Optional[Decimal] = None
    ask_close: Optional[Decimal] = None
    ask_high: Optional[Decimal] = None
    ask_low: Optional[Decimal] = None
    tick_qty: Optional[int] = None


class IndexDaily(BaseModel):
    ts_code: str
    trade_date: date
    close: Optional[Decimal] = None
    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    pre_close: Optional[Decimal] = None
    change: Optional[Decimal] = None
    pct_chg: Optional[Decimal] = None
    vol: Optional[Decimal] = None
    amount: Optional[Decimal] = None


class FinaIndicator(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    end_date: date
    eps: Optional[Decimal] = None
    dt_eps: Optional[Decimal] = None
    total_revenue_ps: Optional[Decimal] = None
    revenue_ps: Optional[Decimal] = None
    bps: Optional[Decimal] = None
    ocfps: Optional[Decimal] = None
    roe: Optional[Decimal] = None
    roe_waa: Optional[Decimal] = None
    roe_dt: Optional[Decimal] = None
    roa: Optional[Decimal] = None
    gross_margin: Optional[Decimal] = None
    netprofit_margin: Optional[Decimal] = None
    grossprofit_margin: Optional[Decimal] = None
    debt_to_assets: Optional[Decimal] = None
    current_ratio: Optional[Decimal] = None
    quick_ratio: Optional[Decimal] = None
    cash_ratio: Optional[Decimal] = None
    assets_turn: Optional[Decimal] = None
    inv_turn: Optional[Decimal] = None
    ar_turn: Optional[Decimal] = None
    roic: Optional[Decimal] = None
    basic_eps_yoy: Optional[Decimal] = None
    dt_eps_yoy: Optional[Decimal] = None
    netprofit_yoy: Optional[Decimal] = None
    dt_netprofit_yoy: Optional[Decimal] = None
    rd_exp: Optional[Decimal] = None
