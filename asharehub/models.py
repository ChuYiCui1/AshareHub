"""Pydantic models matching the AShareHub API response schemas.

These models document the field names and types for each endpoint.
The SDK client returns pd.DataFrame directly (not model instances).
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel


class DailyBar(BaseModel):
    ts_code: str
    trade_date: date
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    pre_close: Optional[float] = None
    change: Optional[float] = None
    pct_chg: Optional[float] = None
    vol: Optional[float] = None
    amount: Optional[float] = None


class Fundamentals(BaseModel):
    ts_code: str
    trade_date: date
    close: Optional[float] = None
    turnover_rate: Optional[float] = None
    turnover_rate_f: Optional[float] = None
    volume_ratio: Optional[float] = None
    pe: Optional[float] = None
    pe_ttm: Optional[float] = None
    pb: Optional[float] = None
    ps: Optional[float] = None
    ps_ttm: Optional[float] = None
    dv_ratio: Optional[float] = None
    dv_ttm: Optional[float] = None
    total_share: Optional[float] = None
    float_share: Optional[float] = None
    free_share: Optional[float] = None
    total_mv: Optional[float] = None
    circ_mv: Optional[float] = None


class MoneyflowHsgt(BaseModel):
    trade_date: date
    ggt_ss: Optional[float] = None
    ggt_sz: Optional[float] = None
    hgt_ss: Optional[float] = None
    hgt_sz: Optional[float] = None
    north_money: Optional[float] = None
    south_money: Optional[float] = None


class ChipDistribution(BaseModel):
    ts_code: str
    trade_date: date
    his_low: Optional[float] = None
    his_high: Optional[float] = None
    cost_5pct: Optional[float] = None
    cost_15pct: Optional[float] = None
    cost_50pct: Optional[float] = None
    cost_85pct: Optional[float] = None
    cost_95pct: Optional[float] = None
    weight_avg: Optional[float] = None
    winner_rate: Optional[float] = None


class FxDaily(BaseModel):
    ts_code: str
    trade_date: date
    bid_open: Optional[float] = None
    bid_close: Optional[float] = None
    bid_high: Optional[float] = None
    bid_low: Optional[float] = None
    ask_open: Optional[float] = None
    ask_close: Optional[float] = None
    ask_high: Optional[float] = None
    ask_low: Optional[float] = None
    tick_qty: Optional[int] = None


class IndexDaily(BaseModel):
    ts_code: str
    trade_date: date
    close: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    pre_close: Optional[float] = None
    change: Optional[float] = None
    pct_chg: Optional[float] = None
    vol: Optional[float] = None
    amount: Optional[float] = None


class FinaIndicator(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    end_date: date
    eps: Optional[float] = None
    dt_eps: Optional[float] = None
    total_revenue_ps: Optional[float] = None
    revenue_ps: Optional[float] = None
    bps: Optional[float] = None
    ocfps: Optional[float] = None
    roe: Optional[float] = None
    roe_waa: Optional[float] = None
    roe_dt: Optional[float] = None
    roa: Optional[float] = None
    gross_margin: Optional[float] = None
    netprofit_margin: Optional[float] = None
    grossprofit_margin: Optional[float] = None
    debt_to_assets: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    cash_ratio: Optional[float] = None
    assets_turn: Optional[float] = None
    inv_turn: Optional[float] = None
    ar_turn: Optional[float] = None
    roic: Optional[float] = None
    basic_eps_yoy: Optional[float] = None
    dt_eps_yoy: Optional[float] = None
    netprofit_yoy: Optional[float] = None
    dt_netprofit_yoy: Optional[float] = None
    rd_exp: Optional[float] = None


class MoneyFlow(BaseModel):
    ts_code: str
    trade_date: date
    buy_sm_vol: Optional[int] = None
    buy_sm_amount: Optional[float] = None
    sell_sm_vol: Optional[int] = None
    sell_sm_amount: Optional[float] = None
    buy_md_vol: Optional[int] = None
    buy_md_amount: Optional[float] = None
    sell_md_vol: Optional[int] = None
    sell_md_amount: Optional[float] = None
    buy_lg_vol: Optional[int] = None
    buy_lg_amount: Optional[float] = None
    sell_lg_vol: Optional[int] = None
    sell_lg_amount: Optional[float] = None
    buy_elg_vol: Optional[int] = None
    buy_elg_amount: Optional[float] = None
    sell_elg_vol: Optional[int] = None
    sell_elg_amount: Optional[float] = None
    net_mf_vol: Optional[int] = None
    net_mf_amount: Optional[float] = None


class NorthboundHolding(BaseModel):
    trade_date: date
    ts_code: str
    name: Optional[str] = None
    vol: Optional[int] = None
    ratio: Optional[float] = None
    exchange: Optional[str] = None


class MarginDetail(BaseModel):
    trade_date: date
    ts_code: str
    name: Optional[str] = None
    rzye: Optional[float] = None
    rqye: Optional[float] = None
    rzmre: Optional[float] = None
    rqyl: Optional[float] = None
    rzche: Optional[float] = None
    rqchl: Optional[float] = None
    rqmcl: Optional[float] = None
    rzrqye: Optional[float] = None


class BlockTrade(BaseModel):
    ts_code: str
    trade_date: date
    price: Optional[float] = None
    vol: Optional[float] = None
    amount: Optional[float] = None
    buyer: Optional[str] = None
    seller: Optional[str] = None


class TopList(BaseModel):
    trade_date: date
    ts_code: str
    name: Optional[str] = None
    close: Optional[float] = None
    pct_change: Optional[float] = None
    turnover_rate: Optional[float] = None
    amount: Optional[float] = None
    l_sell: Optional[float] = None
    l_buy: Optional[float] = None
    l_amount: Optional[float] = None


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
    change_vol: Optional[float] = None
    change_ratio: Optional[float] = None
    after_share: Optional[float] = None
    after_ratio: Optional[float] = None
    avg_price: Optional[float] = None
    total_share: Optional[float] = None
    begin_date: Optional[date] = None
    close_date: Optional[date] = None


class ConceptIndex(BaseModel):
    ts_code: str
    trade_date: date
    name: Optional[str] = None
    leading: Optional[str] = None
    leading_code: Optional[str] = None
    pct_change: Optional[float] = None
    leading_pct: Optional[float] = None
    total_mv: Optional[float] = None
    turnover_rate: Optional[float] = None
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
    adj_factor: Optional[float] = None


class StkFactor(BaseModel):
    ts_code: str
    trade_date: date
    open_hfq: Optional[float] = None
    close_hfq: Optional[float] = None
    high_hfq: Optional[float] = None
    low_hfq: Optional[float] = None
    pre_close_hfq: Optional[float] = None
    open_qfq: Optional[float] = None
    close_qfq: Optional[float] = None
    high_qfq: Optional[float] = None
    low_qfq: Optional[float] = None
    pre_close_qfq: Optional[float] = None
    adj_factor: Optional[float] = None
    macd_dif: Optional[float] = None
    macd_dea: Optional[float] = None
    macd: Optional[float] = None
    kdj_k: Optional[float] = None
    kdj_d: Optional[float] = None
    kdj_j: Optional[float] = None
    rsi_6: Optional[float] = None
    rsi_12: Optional[float] = None
    rsi_24: Optional[float] = None
    boll_upper: Optional[float] = None
    boll_mid: Optional[float] = None
    boll_lower: Optional[float] = None
    cci: Optional[float] = None


class LimitList(BaseModel):
    trade_date: date
    ts_code: str
    industry: Optional[str] = None
    name: Optional[str] = None
    close: Optional[float] = None
    pct_chg: Optional[float] = None
    amount: Optional[float] = None
    limit_amount: Optional[float] = None
    float_mv: Optional[float] = None
    total_mv: Optional[float] = None
    turnover_ratio: Optional[float] = None
    fd_amount: Optional[float] = None
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
    basic_eps: Optional[float] = None
    diluted_eps: Optional[float] = None
    total_revenue: Optional[float] = None
    revenue: Optional[float] = None
    total_cogs: Optional[float] = None
    oper_cost: Optional[float] = None
    sell_exp: Optional[float] = None
    admin_exp: Optional[float] = None
    fin_exp: Optional[float] = None
    rd_exp: Optional[float] = None
    operate_profit: Optional[float] = None
    non_oper_income: Optional[float] = None
    non_oper_exp: Optional[float] = None
    total_profit: Optional[float] = None
    income_tax: Optional[float] = None
    n_income: Optional[float] = None
    n_income_attr_p: Optional[float] = None
    ebit: Optional[float] = None
    ebitda: Optional[float] = None
    update_flag: Optional[str] = None


class BalanceSheet(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    f_ann_date: Optional[date] = None
    end_date: date
    report_type: Optional[str] = None
    comp_type: Optional[str] = None
    total_cur_assets: Optional[float] = None
    money_cap: Optional[float] = None
    notes_receiv: Optional[float] = None
    accounts_receiv: Optional[float] = None
    inventories: Optional[float] = None
    total_nca: Optional[float] = None
    fa_avail_for_sale: Optional[float] = None
    lt_eqt_invest: Optional[float] = None
    fix_assets: Optional[float] = None
    cip: Optional[float] = None
    intan_assets: Optional[float] = None
    goodwill: Optional[float] = None
    total_assets: Optional[float] = None
    total_cur_liab: Optional[float] = None
    st_borr: Optional[float] = None
    notes_payable: Optional[float] = None
    acct_payable: Optional[float] = None
    total_ncl: Optional[float] = None
    lt_borr: Optional[float] = None
    bond_payable: Optional[float] = None
    total_liab: Optional[float] = None
    total_hldr_eqy_exc_min_int: Optional[float] = None
    total_hldr_eqy_inc_min_int: Optional[float] = None
    minority_int: Optional[float] = None
    update_flag: Optional[str] = None


class CashFlow(BaseModel):
    ts_code: str
    ann_date: Optional[date] = None
    f_ann_date: Optional[date] = None
    end_date: date
    report_type: Optional[str] = None
    comp_type: Optional[str] = None
    net_profit: Optional[float] = None
    c_fr_sale_sg: Optional[float] = None
    c_pay_goods_purch_serv_rec: Optional[float] = None
    n_cashflow_act: Optional[float] = None
    c_pay_acq_const_fix_intang_oasset: Optional[float] = None
    c_fr_disp_fix_intang_oasset: Optional[float] = None
    n_cashflow_inv_act: Optional[float] = None
    c_fr_borr: Optional[float] = None
    c_pay_dist_dpcp_int_exp: Optional[float] = None
    n_cash_flows_fnc_act: Optional[float] = None
    n_incr_cash_cash_equ: Optional[float] = None
    c_cash_equ_beg_period: Optional[float] = None
    c_cash_equ_end_period: Optional[float] = None
    free_cashflow: Optional[float] = None
    update_flag: Optional[str] = None


class Forecast(BaseModel):
    ts_code: str
    ann_date: date
    end_date: date
    type: Optional[str] = None
    p_change_min: Optional[float] = None
    p_change_max: Optional[float] = None
    net_profit_min: Optional[float] = None
    net_profit_max: Optional[float] = None
    last_parent_net: Optional[float] = None
    first_ann_date: Optional[date] = None
    summary: Optional[str] = None
    change_reason: Optional[str] = None


class Express(BaseModel):
    ts_code: str
    ann_date: date
    end_date: date
    revenue: Optional[float] = None
    operate_profit: Optional[float] = None
    total_profit: Optional[float] = None
    n_income: Optional[float] = None
    total_assets: Optional[float] = None
    total_hldr_eqy_exc_min_int: Optional[float] = None
    diluted_eps: Optional[float] = None
    diluted_roe: Optional[float] = None
    yoy_net_profit: Optional[float] = None
    bps: Optional[float] = None
    perf_summary: Optional[str] = None
    update_flag: Optional[str] = None


class Dividend(BaseModel):
    ts_code: str
    end_date: date
    ann_date: Optional[date] = None
    div_proc: Optional[str] = None
    stk_div: Optional[float] = None
    stk_bo_rate: Optional[float] = None
    stk_co_rate: Optional[float] = None
    cash_div: Optional[float] = None
    cash_div_tax: Optional[float] = None
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
    weight: Optional[float] = None


class TradeCalendar(BaseModel):
    exchange: str
    cal_date: date
    is_open: int
    pretrade_date: Optional[date] = None
