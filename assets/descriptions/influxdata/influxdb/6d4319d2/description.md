Title
-----
Refactor Points and Rows to dedicated packages

Summary
-------
Extract Point types and parsing logic from `tsdb` package into new `models` package to reduce client dependencies.

Why
---
The Go client has too many transitive dependencies (raft, boltdb, protobuf, bcrypt, etc.) because it imports `tsdb` and `influxql` packages just to work with Point types. Users should not need database engine dependencies to use the client library.

What Changed
------------
- Created new `models` package containing:
  - `Point`, `Tags`, `Fields` types
  - `ParsePoints()`, `ParsePointsString()`, `ParsePointsWithPrecision()`
  - Point marshaling/unmarshaling logic
  - Tag and field encoding/escaping
  
- Created `pkg/escape` package for string escape utilities

- Updated imports throughout codebase:
  - `client/` → now imports `models` instead of `tsdb`
  - `cluster/`, `services/*`, `tsdb/*` → updated to use `models.Point`
  - All `tsdb.Point` → `models.Point`
  - All `tsdb.Tags` → `models.Tags`  
  - All `tsdb.Fields` → `models.Fields`

- Moved functionality:
  - `tsdb/points.go` → `models/points.go`
  - `tsdb/points_test.go` → `models/points_test.go`
  - Escape codes → `pkg/escape`

Benefits
--------
- Client package dependency graph significantly reduced
- Clean separation: data models vs storage engine
- Client users no longer pull in database internals
- Maintains backward compatibility in `tsdb` package