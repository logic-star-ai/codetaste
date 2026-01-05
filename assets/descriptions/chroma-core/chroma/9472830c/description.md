# Refactor Rust Codebase into Workspace Crates

## Summary
Split monolithic Rust worker codebase into workspace crates for improved modularity and maintainability.

## Background
Rust benchmarks require library targets, and the single-crate structure made it impossible to write benchmarks against individual modules (e.g., FTS index) without exposing everything. The codebase needed better separation of concerns.

## Changes
Created workspace with 7 new crates:
- `chroma-blockstore` - Arrow blockfile implementation, sparse indexes, delta storage
- `chroma-cache` - Cache abstraction (Unbounded, LRU, LFU via foyer)
- `chroma-config` - `Configurable` trait
- `chroma-error` - `ChromaError` trait and `ErrorCodes` enum
- `chroma-storage` - S3/local storage abstraction
- `chroma-types` - Core types (LogRecord, Segment, Collection, Metadata, DataRecord, Chunk) + proto codegen
- `worker` - Orchestration, operators, execution, system

### Structure
```
rust/
├── blockstore/    (from worker/src/blockstore)
├── cache/         (from worker/src/cache)
├── config/        (extracted from worker/src/config)
├── error/         (from worker/src/errors)
├── storage/       (from worker/src/storage)
├── types/         (from worker/src/types + data_chunk + DataRecord)
└── worker/        (remaining orchestration code)
```

### Key Technical Changes
- Workspace `Cargo.toml` with shared dependency specifications
- Updated imports: `crate::*` → `chroma_*::*` across codebase
- Visibility: `pub(crate)` → `pub` where needed for cross-crate access
- Proto generation moved to `chroma-types` build script
- Docker builds updated to accommodate multi-crate structure

### What's Deferred
Some `pub(crate)` items may still need promotion to `pub` - handling on-demand rather than exhaustive audit.

## Benefits
- ✅ Enables crate-level benchmarking
- ✅ Clearer dependency boundaries
- ✅ Better code organization
- ✅ Reusable components across binaries
- ✅ Faster incremental builds (potential)