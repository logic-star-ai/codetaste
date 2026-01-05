# Refactor streaming multi-scan directory structure

## Summary

Restructure the `multi_scan` (formerly `multi_file_reader`) module with improved organization and consistent naming. This is a code movement refactor with no logic changes.

## Why

- Previous structure had become unwieldy and hard to navigate
- Terminology was inconsistent (`MultiFile` vs `MultiScan` - consolidate to `MultiScan`)
- Related components were scattered across different directories
- Pipeline initialization logic was not clearly separated from execution logic

## Changes

### Module Restructure

```
multi_file_reader/              →  multi_scan/
├── extra_ops/                  →  ├── components/          (encapsulated logic)
│   ├── apply.rs                   │   ├── apply_extra_ops.rs
│   ├── column_selector.rs         │   ├── bridge.rs
│   └── ...                        │   ├── column_selector.rs
├── initialization/             →  │   ├── errors.rs
│   ├── deletion_files.rs          │   ├── forbid_extra_columns.rs
│   ├── predicate.rs               │   ├── physical_slice.rs
│   ├── projection.rs              │   ├── projection/{mod.rs,builder.rs}
│   └── slice.rs                   │   ├── reader_operation_pushdown.rs
├── reader_pipelines/           →  │   ├── row_counter.rs
│   └── generic.rs                 │   └── row_deletions.rs
├── post_apply_pipeline/        →  ├── config.rs            (extracted config)
├── bridge.rs                   →  ├── functions/           (standalone functions)
├── row_counter.rs              →  │   ├── resolve_projections.rs
└── ...                            │   └── resolve_slice.rs
                                   ├── pipeline/            (pipeline orchestration)
                                   │   ├── initialization.rs
                                   │   ├── models.rs
                                   │   └── tasks/
                                   │       ├── attach_reader_to_bridge.rs
                                   │       ├── bridge.rs
                                   │       ├── post_apply_extra_ops.rs
                                   │       └── reader_starter.rs
                                   └── reader_interface/    (unchanged)
```

### Naming Changes

- `MultiFileReader{,Config}` → `MultiScan{,Config}`
- `PostApplyPipeline` → `PostApplyExtraOps`
- `send_phase_tx_to_bridge` → `phase_channel_tx`
- `join_handle` → `task_handle`
- Minor typo fix: "scans executors" → "scan executors"

### Key Improvements

- Clear separation of concerns: components / config / functions / pipeline
- Pipeline initialization logic centralized in `pipeline/initialization.rs`
- Tasks properly organized in `pipeline/tasks/`
- Error handling extracted to `components/errors.rs`
- Models extracted to `pipeline/models.rs`