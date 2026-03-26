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


class MoneyFlow(BaseModel):
    ts_code: str
    trade_date: date
    buy_sm_vol: Optional[int] = None
    buy_sm_amount: Optional[Decimal] = None
    sell_sm_vol: Optional[int] = None
    sell_sm_amount: Optional[Decimal] = None
    buy_md_vol: Optional[int] = None
    buy_md_amount: Optional[Decimal] = None
    sell_md_vol: Optional[int] = None
    sell_md_amount: Optional[Decimal] = None
    buy_lg_vol: Optional[int] = None
    buy_lg_amount: Optional[Decimal] = None
    sell_lg_vol: Optional[int] = None
    sell_lg_amount: Optional[Decimal] = None
    buy_elg_vol: Optional[int] = None
    buy_elg_amount: Optional[Decimal] = None
    sell_elg_vol: Optional[int] = None
    sell_elg_amount: Optional[Decimal] = None
    net_mf_vol: Optional[int] = None
    net_mf_amount: Optional[Decimal] = None


class NorthboundHolding(BaseModel):
    trade_date: date
    ts_code: str
    name: Optional[str] = None
    vol: Optional[int] = None
    ratio: Optional[Decimal] = None
    exchange: Optional[str] = None


class MarginDetail(BaseModel):
    trade_date: date
    ts_code: str
    name: Optional[str] = None
    rzye: Optional[Decimal] = None
    rqye: Optional[Decimal] = None
    rzmre: Optional[Decimal] = None
    rqyl: Optional[Decimal] = None
    rzche: Optional[Decimal] = None
    rqchl: Optional[Decimal] = None
    rqmcl: Optional[Decimal] = None
    rzrqye: Optional[Decimal] = None


class BlockTrade(BaseModel):
    ts_code: str
    trade_date: date
    price: Optional[Decimal] = None
    vol: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    buyer: Optional[str] = None
    seller: Optional[str] = None


class TopList(BaseModel):
    trade_date: date
    ts_code: str
    name: Optional[str] = None
    close: Optional[Decimal] = None
    pct_change: Optional[Decimal] = None
    turnover_rate: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    l_sell: Optional[Decimal] = None
    l_buy: Optional[Decimal] = None
    l_amount: Optional[Decimal] = None


class ShareholderNumber(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    end_date: date
    holder_num: Optional[int] = None


class HolderTrade(BaseModel):
    ts_code: str
    ann_date: date
    holder_name: Optional[str] = None
    holder_type: Optional[str] = None
    in_de: Optional[str] = None
    change_vol: Optional[Decimal] = None
    change_ratio: Optional[Decimal] = None
    after_share: Optional[Decimal] = None
    after_ratio: Optional[Decimal] = None
    avg_price: Optional[Decimal] = None
    total_share: Optional[Decimal] = None
    begin_date: Optional[date] = None
    close_date: Optional[date] = None


class ConceptIndex(BaseModel):
    ts_code: str
    trade_date: date
    name: Optional[str] = None
    leading: Optional[str] = None
    leading_code: Optional[str] = None
    pct_change: Optional[Decimal] = None
    leading_pct: Optional[Decimal] = None
    total_mv: Optional[Decimal] = None
    turnover_rate: Optional[Decimal] = None
    up_num: Optional[int] = None
    down_num: Optional[int] = None
    idx_type: Optional[str] = None
    level: Optional[str] = None


class ConceptMember(BaseModel):
    trade_date: date
    ts_code: str
    con_code: str
    name: Optional[str] = None


class StockBasic(BaseModel):
    ts_code: str
    symbol: Optional[str] = None
    name: Optional[str] = None
    area: Optional[str] = None
    industry: Optional[str] = None
    fullname: Optional[str] = None
    enname: Optional[str] = None
    cnspell: Optional[str] = None
    market: Optional[str] = None
    exchange: Optional[str] = None
    curr_type: Optional[str] = None
    list_status: Optional[str] = None
    list_date: Optional[date] = None
    delist_date: Optional[date] = None
    is_hs: Optional[str] = None


class IndustryClassification(BaseModel):
    ts_code: str
    name: Optional[str] = None
    l1_code: Optional[str] = None
    l1_name: Optional[str] = None
    l2_code: Optional[str] = None
    l2_name: Optional[str] = None
    l3_code: Optional[str] = None
    l3_name: Optional[str] = None
