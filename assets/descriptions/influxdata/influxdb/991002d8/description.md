Title
-----
Refactor: Move series file to its own package

Summary
-------
Extract series file functionality from `tsdb` package into dedicated `tsdb/seriesfile` package to improve code organization and reduce package dependencies.

Why
---
Series file code is a distinct subsystem that can be isolated. Moving it to its own package:
- Improves modularity and separation of concerns
- Makes dependencies more explicit and clearer
- Reduces coupling in the `tsdb` package
- Follows better package organization patterns

What Changed
------------
**New Package Structure:**
- Created `tsdb/seriesfile/` package
- Moved series file implementation and related types

**Types Moved to `seriesfile` package:**
- `SeriesFile`, `SeriesPartition`, `SeriesSegment`
- `SeriesIndex`, `SeriesIndexHeader`
- `SeriesPartitionCompactor`, `Verify`
- Functions: `ParseSeriesKey`, `AppendSeriesKey`, `CompareSeriesKeys`, `GenerateSeriesKeys`, etc.

**Files Relocated:**
- `series_file.go` → `seriesfile/series_file.go`
- `series_file_metrics.go` → `seriesfile/metrics.go`
- `series_index.go` → `seriesfile/series_index.go`
- `series_partition.go` → `seriesfile/series_partition.go`
- `series_segment.go` → `seriesfile/series_segment.go`
- `series_verify.go` → `seriesfile/series_verify.go`
- ...and corresponding test files

**Import Updates:**
- Updated imports across codebase: `tsdb.*` → `seriesfile.*`
- Updated references in: `cmd/influx*`, `storage/`, `tsdb/tsi1/`, `tsdb/tsm1/`, `mock/`, etc.

**Additional Cleanup:**
- Moved `ByTagKey` type to `tsdb/tsi1` (only usage location)
- Removed unused `SeriesIDElems` type
- Inlined `ReadAllSeriesIDIterator` (single usage)
- Removed `platform` → `influxdb` import aliases
- Moved `filterUndeletedSeriesIDIterator` to `tsi1` package