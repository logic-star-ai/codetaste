# Remove BuildContext Abstraction

## Summary

Remove the `BuildContext` struct that was used to pass configuration during operator building. Replace with direct `*zap.SugaredLogger` parameter in `Build()` methods.

## Why

BuildContext was originally designed to bundle logger, parameters, database file, namespace info, etc. for operator construction. Over time it was stripped of functionality and now only carries a logger, making it an unnecessary abstraction layer.

## Changes

**Core Removals**
- Delete `operator/build_context.go` and associated tests
- Remove `BuildContext` struct with `Logger`, `DefaultOutputIDs`, helper methods (`WithDefaultOutputIDs()`, `Copy()`)

**API Updates**
- Change `Build()` signature across all operators: `Build(operator.BuildContext)` → `Build(*zap.SugaredLogger)`
- Update `operator.Builder` interface accordingly

**Affected Operators**
- All input operators: `file`, `generate`, `journald`, `k8sevent`, `stdin`, `syslog`, `tcp`, `udp`, `windows`
- All output operators: `drop`, `file`, `stdout`
- All parser operators: `csv`, `json`, `regex`, `severity`, `time`, `trace`, `uri`, `syslog`
- All transformer operators: `add`, `copy`, `filter`, `flatten`, `metadata`, `move`, `noop`, `recombine`, `remove`, `restructure`, `retain`, `router`

**Helper Updates**
- Update helper configs: `InputConfig`, `OutputConfig`, `ParserConfig`, `TransformerConfig`, `WriterConfig`
- Update `EncodingConfig.Build()` to remove context parameter
- Update validator methods: `TimeParser.Validate()`, `TraceParser.Validate()` to remove context dependency

**Pipeline Changes**
- Move default output handling from `BuildContext.DefaultOutputIDs` into `pipeline.Config.Build()`
- Consolidate `BuildOperators()` logic into `Build()`
- Remove `SetOutputIDs()` helper function

**Test Updates**
- Replace `testutil.NewBuildContext(t)` with `testutil.Logger(t)` throughout test suite
- Update mock operator builder interface

## Result

Simplified codebase with ~650 lines removed, clearer Build method signatures, and eliminated unnecessary indirection layer.