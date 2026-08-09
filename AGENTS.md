# Repository instructions

## Public code-field compatibility invariant

Treat this as a stable, non-negotiable public contract across the API, SDK,
MCP tools, documentation, skills, examples, and tests.

- Public primary codes use `symbol`, including stocks, indices, Eastmoney
  sectors such as `BK0949.DC`, ETFs, and other instrument types.
- When a record or request has a second constituent security, use
  `con_symbol`.
- Do not replace public `symbol` with `index_code`, `bk_code`, `board_code`, or
  another type-specific alias.
- Do not replace public `con_symbol` with `con_code`.
- The SDK and MCP follow the same public naming, including
  `concepts(symbol=...)` and
  `concept_members(symbol=..., con_symbol=...)`.
- Tushare ingestion, RDS columns, and the legacy V1 compatibility layer may
  keep source-native `ts_code`, `index_code`, and `con_code`. Translate those
  internal names only at the public boundary.
- Preserve this contract for backward compatibility. Do not add rejection or
  replacement hints that force existing callers onto type-specific names.

Any change to this contract must update API validation, OpenAPI output, SDK,
MCP, documentation, skills, smoke tests, and unit tests together.
