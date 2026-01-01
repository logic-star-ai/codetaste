# Remove `common_error::prelude` module

## Summary
Remove the `prelude` module from `common-error` crate and replace all prelude imports with explicit imports throughout the codebase.

## Why
Most re-exports in the `prelude` module are seldom used. Explicit imports improve code clarity and make dependencies more transparent.

## Changes

- **Remove `prelude` module** from `src/common/error/src/lib.rs`
- **Move constants** (`INNER_ERROR_CODE`, `INNER_ERROR_MSG`) to crate root
- **Replace prelude imports** across ~80+ files with explicit imports:
  - `common_error::ext::{BoxedError, ErrorExt, PlainError}`
  - `common_error::status_code::StatusCode`
  - `snafu::{Location, Snafu, ResultExt, OptionExt, ErrorCompat, ...}`

## Affected Components
- `api`, `catalog`, `client`, `cmd`, `common/*`, `datanode`, `datatypes`
- `file-table-engine`, `frontend`, `log-store`, `meta-*`, `mito*`
- `partition`, `promql`, `query`, `script`, `servers`, `sql`, `storage`
- `store-api`, `table-procedure`, `table`