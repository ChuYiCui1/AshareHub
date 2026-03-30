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


class AdjFactor(BaseModel):
    ts_code: str
    trade_date: date
    adj_factor: Optional[Decimal] = None


class StkFactor(BaseModel):
    ts_code: str
    trade_date: date
    open_hfq: Optional[Decimal] = None
    close_hfq: Optional[Decimal] = None
    high_hfq: Optional[Decimal] = None
    low_hfq: Optional[Decimal] = None
    pre_close_hfq: Optional[Decimal] = None
    open_qfq: Optional[Decimal] = None
    close_qfq: Optional[Decimal] = None
    high_qfq: Optional[Decimal] = None
    low_qfq: Optional[Decimal] = None
    pre_close_qfq: Optional[Decimal] = None
    adj_factor: Optional[Decimal] = None
    macd_dif: Optional[Decimal] = None
    macd_dea: Optional[Decimal] = None
    macd: Optional[Decimal] = None
    kdj_k: Optional[Decimal] = None
    kdj_d: Optional[Decimal] = None
    kdj_j: Optional[Decimal] = None
    rsi_6: Optional[Decimal] = None
    rsi_12: Optional[Decimal] = None
    rsi_24: Optional[Decimal] = None
    boll_upper: Optional[Decimal] = None
    boll_mid: Optional[Decimal] = None
    boll_lower: Optional[Decimal] = None
    cci: Optional[Decimal] = None


class LimitList(BaseModel):
    trade_date: date
    ts_code: str
    industry: Optional[str] = None
    name: Optional[str] = None
    close: Optional[Decimal] = None
    pct_chg: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    limit_amount: Optional[Decimal] = None
    float_mv: Optional[Decimal] = None
    total_mv: Optional[Decimal] = None
    turnover_ratio: Optional[Decimal] = None
    fd_amount: Optional[Decimal] = None
    first_time: Optional[str] = None
    last_time: Optional[str] = None
    open_times: Optional[int] = None
    up_stat: Optional[str] = None
    limit_times: Optional[int] = None
    limit: Optional[str] = None


class IncomeStatement(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    f_ann_date: Optional[date] = None
    end_date: date
    report_type: Optional[str] = None
    comp_type: Optional[str] = None
    basic_eps: Optional[Decimal] = None
    diluted_eps: Optional[Decimal] = None
    total_revenue: Optional[Decimal] = None
    revenue: Optional[Decimal] = None
    total_cogs: Optional[Decimal] = None
    oper_cost: Optional[Decimal] = None
    sell_exp: Optional[Decimal] = None
    admin_exp: Optional[Decimal] = None
    fin_exp: Optional[Decimal] = None
    rd_exp: Optional[Decimal] = None
    operate_profit: Optional[Decimal] = None
    non_oper_income: Optional[Decimal] = None
    non_oper_exp: Optional[Decimal] = None
    total_profit: Optional[Decimal] = None
    income_tax: Optional[Decimal] = None
    n_income: Optional[Decimal] = None
    n_income_attr_p: Optional[Decimal] = None
    ebit: Optional[Decimal] = None
    ebitda: Optional[Decimal] = None
    update_flag: Optional[str] = None


class BalanceSheet(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    f_ann_date: Optional[date] = None
    end_date: date
    report_type: Optional[str] = None
    comp_type: Optional[str] = None
    total_cur_assets: Optional[Decimal] = None
    money_cap: Optional[Decimal] = None
    notes_receiv: Optional[Decimal] = None
    accounts_receiv: Optional[Decimal] = None
    inventories: Optional[Decimal] = None
    total_nca: Optional[Decimal] = None
    fa_avail_for_sale: Optional[Decimal] = None
    lt_eqt_invest: Optional[Decimal] = None
    fix_assets: Optional[Decimal] = None
    cip: Optional[Decimal] = None
    intan_assets: Optional[Decimal] = None
    goodwill: Optional[Decimal] = None
    total_assets: Optional[Decimal] = None
    total_cur_liab: Optional[Decimal] = None
    st_borr: Optional[Decimal] = None
    notes_payable: Optional[Decimal] = None
    acct_payable: Optional[Decimal] = None
    total_ncl: Optional[Decimal] = None
    lt_borr: Optional[Decimal] = None
    bond_payable: Optional[Decimal] = None
    total_liab: Optional[Decimal] = None
    total_hldr_eqy_exc_min_int: Optional[Decimal] = None
    total_hldr_eqy_inc_min_int: Optional[Decimal] = None
    minority_int: Optional[Decimal] = None
    update_flag: Optional[str] = None


class CashFlow(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    f_ann_date: Optional[date] = None
    end_date: date
    report_type: Optional[str] = None
    comp_type: Optional[str] = None
    net_profit: Optional[Decimal] = None
    c_fr_sale_sg: Optional[Decimal] = None
    c_pay_goods_purch_serv_rec: Optional[Decimal] = None
    n_cashflow_act: Optional[Decimal] = None
    c_pay_acq_const_fix_intang_oasset: Optional[Decimal] = None
    c_fr_disp_fix_intang_oasset: Optional[Decimal] = None
    n_cashflow_inv_act: Optional[Decimal] = None
    c_fr_borr: Optional[Decimal] = None
    c_pay_dist_dpcp_int_exp: Optional[Decimal] = None
    n_cash_flows_fnc_act: Optional[Decimal] = None
    n_incr_cash_cash_equ: Optional[Decimal] = None
    c_cash_equ_beg_period: Optional[Decimal] = None
    c_cash_equ_end_period: Optional[Decimal] = None
    free_cashflow: Optional[Decimal] = None
    update_flag: Optional[str] = None


class Forecast(BaseModel):
    ts_code: str
    ann_date: date
    end_date: date
    type: Optional[str] = None
    p_change_min: Optional[Decimal] = None
    p_change_max: Optional[Decimal] = None
    net_profit_min: Optional[Decimal] = None
    net_profit_max: Optional[Decimal] = None
    last_parent_net: Optional[Decimal] = None
    first_ann_date: Optional[date] = None
    summary: Optional[str] = None
    change_reason: Optional[str] = None


class Express(BaseModel):
    ts_code: str
    ann_date: date
    end_date: date
    revenue: Optional[Decimal] = None
    operate_profit: Optional[Decimal] = None
    total_profit: Optional[Decimal] = None
    n_income: Optional[Decimal] = None
    total_assets: Optional[Decimal] = None
    total_hldr_eqy_exc_min_int: Optional[Decimal] = None
    diluted_eps: Optional[Decimal] = None
    diluted_roe: Optional[Decimal] = None
    yoy_net_profit: Optional[Decimal] = None
    bps: Optional[Decimal] = None
    perf_summary: Optional[str] = None
    update_flag: Optional[str] = None


class Dividend(BaseModel):
    ts_code: str
    end_date: date
    ann_date: Optional[date] = None
    div_proc: Optional[str] = None
    stk_div: Optional[Decimal] = None
    stk_bo_rate: Optional[Decimal] = None
    stk_co_rate: Optional[Decimal] = None
    cash_div: Optional[Decimal] = None
    cash_div_tax: Optional[Decimal] = None
    record_date: Optional[date] = None
    ex_date: Optional[date] = None
    pay_date: Optional[date] = None
    div_listdate: Optional[date] = None
    imp_ann_date: Optional[date] = None


class IndexWeight(BaseModel):
    index_code: str
    trade_date: date
    con_code: str
    con_name: Optional[str] = None
    weight: Optional[Decimal] = None


class TradeCalendar(BaseModel):
    exchange: str
    cal_date: date
    is_open: int
    pretrade_date: Optional[date] = None
