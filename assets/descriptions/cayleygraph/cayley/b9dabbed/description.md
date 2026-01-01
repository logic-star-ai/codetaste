# Rename `graph.Value` to `graph.Ref` to reduce naming ambiguity

## Summary

Rename the `graph.Value` type to `graph.Ref` throughout the codebase. The name `Value` was confusing given the existence of `quad.Value`, and `Ref` more accurately describes its purpose as an opaque reference token.

## Why

- **Naming collision**: `graph.Value` and `quad.Value` caused confusion
- **Semantic clarity**: The type represents an opaque reference/token to nodes/quads in the backing store, not a "value" in the traditional sense
- **Better intent**: "Ref" (reference) conveys that it's a pointer-like abstraction managed by the QuadStore

## Changes

- Rename `graph.Value` interface → `graph.Ref`
- Update all function signatures accepting/returning `graph.Value` → `graph.Ref`
- Update all collections (`[]graph.Value` → `[]graph.Ref`, `map[string]graph.Value` → `map[string]graph.Ref`)
- Maintain backward compatibility via type alias: `type Value = Ref` with deprecation notice
- Update comments and documentation to reference `Ref` instead of `Value`

## Scope

- `graph/` package core types and interfaces
- All iterator implementations (`graph/iterator/`, `graph/kv/`, `graph/memstore/`, `graph/nosql/`, `graph/sql/`, `graph/gaedatastore/`)
- Path operations (`graph/path/`)
- Query engines (`query/gizmo/`, `query/mql/`, `query/sexp/`, `query/graphql/`)
- Shape optimization (`graph/shape/`)
- Test mocks (`graph/graphmock/`, `graph/graphtest/`)
- Commands (`cmd/cayley/command/`)
- Schema loader (`schema/`)
- Utilities (`internal/gephi/`)

## Compatibility

Add deprecated alias to maintain backward compatibility:
```go
// Deprecated: use Ref instead.
type Value = Ref
```