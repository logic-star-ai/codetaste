# Title
Refactor: Break up and flatten `internal` package structure

# Summary
Reorganize the `internal` directory by splitting the monolithic `internal` package into focused, purpose-specific packages and flattening nested package hierarchies.

# Why
The `internal` directory should be a namespace for internal packages, not a catch-all package itself. Using `internal` as an actual package risks becoming a dumping ground for miscellaneous code that doesn't obviously fit elsewhere.

# Changes

## Split `internal` package into focused packages
- `internal/bsonutil` - BSON utility functions (e.g., `StringSliceFromRawValue`, `RawToDocuments`)
- `internal/csfle` - Client-side field level encryption utilities
- `internal/csot` - Client-side operation timeout utilities
- `internal/errutil` - Error handling utilities (`WrapErrorf`, `UnwrapError`, etc.)
- `internal/handshake` - Handshake-related constants (`LegacyHello`, `LegacyHelloLowercase`)
- `internal/httputil` - HTTP client utilities

## Flatten nested package hierarchies
- `internal/testutil/monitor` → `internal/eventtest`
- `internal/randutil/rand` → `internal/rand`
- `internal/testutil/israce` → `internal/israce`
- `internal/testutil/helpers` → `internal/spectest`
- `internal/testutil` → `internal/integtest`

## Relocate single-use code
- Move code from `internal/` that's only used in one package directly into that package
- Move `internal/background_context.go` → `mongo/background_context.go`
- Move `internal/cancellation_listener.go` → `x/mongo/driver/topology/connection.go` (as `cancellListener`)

## Cleanup
- Remove unused `internal.MultiError` function and related code
- Move `LegacyNotPrimary` error message constant to `x/mongo/driver/errors.go`
- Rename `helpers.AssertSoon` → `assert.Soon` with minor behavior change (uses `t.Error` instead of `t.Fail`)

## Update imports
- Update all import paths across the codebase to reference new package locations
- Update `.golangci.yml` linter configuration for new paths