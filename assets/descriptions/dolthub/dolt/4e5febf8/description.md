# Title
Refactor sysbench_runner and tpcc_runner into unified benchmark_runner

# Summary
Consolidate `sysbench_runner` and `tpcc_runner` into a single `benchmark_runner` package with improved architecture, reduced duplication, and better profiling support.

# Why
- Two separate tools (`sysbench_runner` and `tpcc_runner`) had significant code duplication
- File-based JSON configuration made testing difficult
- Profiling support was incomplete/broken
- Architecture needed better separation of concerns
- Preparation for PGO (Profile-Guided Optimization) dolt releases

# Changes

## Consolidation
- Renamed `go/performance/utils/sysbench_runner` → `go/performance/utils/benchmark_runner`
- Removed `go/performance/utils/tpcc_runner` entirely
- Merged TPCC functionality into unified benchmark_runner

## Architecture Improvements
- Introduced `Benchmarker` interface for running benchmarks
- Introduced `Config`, `SysbenchConfig`, `TpccConfig` interfaces
- Split `ServerConfig` into specialized interfaces:
  - `ServerConfig` (base)
  - `InitServerConfig` (for servers needing init, e.g., Postgres)
  - `ProtocolServerConfig` (for connection protocol configuration)
  - `ProfilingServerConfig` (for profiling support)
- Created separate benchmarker implementations per server+test type:
  - `doltBenchmarkerImpl`, `mysqlBenchmarkerImpl`, `doltgresBenchmarkerImpl`, `postgresBenchmarkerImpl`
  - `doltTpccBenchmarkerImpl`, `mysqlTpccBenchmarkerImpl`

## Configuration Changes
- **Removed** file-based JSON configuration
- **Removed** command-line executables
- Now uses programmatic configuration through interfaces
- Testing via Go tests in `run_tests.go` instead of CI config files

## Code Deduplication
- Extracted common server management → `server.go`
- Unified test execution logic → `Tester` interface, `sysbench.go`, `tpcc.go`
- Consolidated result handling across benchmark types

## API Changes
- `Run(ctx, SysbenchConfig)` - runs sysbench tests
- `RunTpcc(ctx, TpccConfig)` - runs TPCC tests
- `Profile(ctx, ...)` - profiles Dolt server during benchmarks

## Profiling
- Fixed and improved CPU profiling support for Dolt
- Proper profile merging and output
- CPU profile written to configurable path

## Testing
- Comprehensive test coverage in `run_test.go`
- Tests for Dolt+MySQL sysbench combinations
- Tests for Doltgres+Postgres combinations
- Tests for TPCC benchmarks
- Tests for profiling