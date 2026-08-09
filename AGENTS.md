# Repository instructions

## Eastmoney sector code naming invariant

Treat this as a stable, non-negotiable public contract across the API, SDK,
MCP tools, documentation, skills, examples, and tests.

- An Eastmoney sector code such as `BK0949.DC` is always named `bk_code`.
- Never accept or return a `BKxxxx.DC` value under `symbol`.
- In Eastmoney sector-constituent APIs, keep the constituent stock field named
  `con_code`, such as `000001.SZ`; do not rename it to `symbol` or
  `con_symbol`.
- Do not introduce `board_code` or `sector_code` as aliases for
  `bk_code`.
- V2 public requests and responses use `bk_code` for the sector and `con_code`
  for the constituent stock. Reject `symbol` and `con_symbol` on Eastmoney
  sector-constituent endpoints with HTTP 422 instead of silently translating
  them.
- The SDK and MCP follow the same public naming:
  `concepts(bk_code=...)` and
  `concept_members(bk_code=..., con_code=...)`.
- Tushare ingestion, RDS columns, and the legacy V1 compatibility layer keep
  their source-native `ts_code` and `con_code` names. At the public boundary,
  translate only sector `ts_code` to `bk_code`; keep `con_code` unchanged.
- `con_symbol` may remain in unrelated index/ETF constituent contracts. It
  must not be used for Eastmoney sector constituents.

Any change to this contract must update API validation, OpenAPI output, SDK,
MCP, documentation, skills, smoke tests, and unit tests together.
