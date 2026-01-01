# Title

Refactor: Introduce `UnifiedScanArgs` to consolidate scan arguments

## Summary

Replace `FileScanOptions` with `UnifiedScanArgs` to contain arguments common to all scan types. This centralizes scan configuration and simplifies adding features across different file formats.

## Why

- Adding new features to scans required updating multiple enum variants and file-type-specific code
- `FileScanOptions` was scattered across different scan implementations
- Inconsistent handling of common scan parameters (e.g., `cloud_options` was inside each scan type variant)
- Simplifies maintenance and reduces code duplication

## Changes

**Core Refactoring**
- Rename `FileScanOptions` → `UnifiedScanArgs`
- Move `cloud_options` from individual scan type enum variants (`FileScan::Parquet`, `FileScan::Csv`, etc.) into `UnifiedScanArgs`
- All scan types now share the same `UnifiedScanArgs` structure

**Field Changes**
- `with_columns` → `projection` (clearer naming)
- `allow_missing_columns: bool` → `missing_columns_policy: MissingColumnsPolicy` (enum for extensibility)
- `pre_slice: Option<(i64, usize)>` → `pre_slice: Option<Slice>` (use typed enum instead of tuple)
- Remove `file_counter` field
- Add `schema: Option<SchemaRef>` (user-provided schema, inferred during IR conversion if None)
- Add `cast_columns_policy: CastColumnsPolicy`

**Policy Types**
- Introduce `MissingColumnsPolicy` enum: `Raise` | `Insert`
- Introduce `CastColumnsPolicy` enum: `ErrorOnMismatch`
- Introduce `ExtraColumnsPolicy` enum: `Raise` | `Ignore`

**HiveOptions**
- Add `HiveOptions::new_enabled()` and `HiveOptions::new_disabled()` constructors

**Updates Across Codebase**
- Update all scan builders (CSV, Parquet, IPC, NDJson, Anonymous) to use `UnifiedScanArgs`
- Update streaming engine nodes to use new structure
- Update Python bindings (version bump to 7.0 for breaking IR changes)
- Update optimization passes, formatters, and visitors

## Out of Scope

- LazyFileListReaders still need updates (follow-up PR)
- Additional policy configurations beyond those introduced here