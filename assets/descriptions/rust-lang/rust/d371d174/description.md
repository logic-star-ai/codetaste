# Refactor TLS implementation to improve maintainability and modularity

## Summary

Consolidate platform-specific TLS (Thread-Local Storage) code into a unified, modular structure under `sys/thread_local/` to simplify future porting efforts and reduce code duplication.

## Why

Current TLS implementation is fragmented across multiple platform-specific `thread_local_key`/`thread_local_dtor` modules, forcing porters to copy entire (often suboptimal) implementations. This creates maintenance burden and inconsistency.

## Changes

### Module Reorganization
- Move all `thread_local_{key,dtor}` modules → `sys/thread_local/`
- Create clear hierarchy:
  - `destructors/` - destructor registration strategies
  - `guard/` - platform-specific destructor scheduling  
  - `key/` - TLS key implementations
  - Main impls: `native/`, `os.rs`, `statik.rs`

### Cleanup Deleted Files
- Remove platform-specific modules from:
  - `sys/pal/{hermit,itron,sgx,solid,teeos,uefi,unix,unsupported,wasi*,wasm,windows,xous,zkvm}/thread_local_*`
  - `sys_common/thread_local_{key,dtor}.rs`

### Implementation Improvements
- Key-based destructor fallback: store list in `#[thread_local]` static instead of in key (eliminates indirection)
- ZKVM: switch to WebAssembly-style implementation

### Documentation
- Add comprehensive module docs explaining:
  - Three TLS implementation strategies (static/native/OS)
  - Platform-specific abstractions
  - Destructor registration mechanisms

## Result

Future porters can mix-and-match existing implementations instead of copying entire modules. Clear separation of concerns makes the codebase more maintainable.