# Refactor diagnostic tools from test packaging to new hbase-diagnostics module

## Summary
Move performance evaluation and load testing tools from test packages to a new dedicated `hbase-diagnostics` module to make them available in binary distributions without including test JARs.

## Why
- Tools like `PerformanceEvaluation`, `LoadTestTool`, `HFilePerformanceEvaluation`, `ScanPerformanceEvaluation`, `LoadBalancerPerformanceEvaluation`, and `WALPerformanceEvaluation` are valuable diagnostic utilities
- Currently buried in test JARs, causing unnecessary bloat in assemblies
- Test JARs introduce CVE-prone dependencies into binary distributions
- Need clean separation between production tooling and test infrastructure

## Changes
- Create new `hbase-diagnostics` module
- Move diagnostic tools from `src/test/java` → `src/main/java`:
  - `PerformanceEvaluation` (from hbase-mapreduce)
  - `LoadTestTool` (from hbase-mapreduce)
  - `HFilePerformanceEvaluation` (from hbase-server)
  - `ScanPerformanceEvaluation` (from hbase-mapreduce)
  - `LoadBalancerPerformanceEvaluation` (from hbase-balancer)
  - `WALPerformanceEvaluation` (from hbase-server)
  - Supporting classes: `MultiThreaded*`, `LoadTest*`, data generators, etc.
- Extract shared utilities to break cyclic dependencies:
  - `LoadTestUtil` (table creation helpers)
  - `KerberosUtils` (authentication)
  - `WALPerformanceEvaluationUtil` (filesystem setup)
- Rename `KeyProviderForTesting` → `MockAesKeyProvider`
- Move `RandomDistribution`, `LoadTestKVGenerator`, `MockRegionServerServices`, `FilterAllFilter` to main source
- Update imports and dependencies across modules
- Add to assembly configuration
- Add `@InterfaceAudience.Private` annotations