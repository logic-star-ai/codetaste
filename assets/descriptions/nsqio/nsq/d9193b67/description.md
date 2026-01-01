# Reorganize internal packages

## Summary
Break up the monolithic `internal/util` package into focused, purpose-specific packages with clear boundaries.

## Changes

### Package Migrations
- `internal/util` → `internal/app` - app-level utilities (StringArray, FloatArray, ParseOpts, Logger)
- `internal/util` → `internal/http_api` - HTTP API utilities (request/response handling, ReqParams, topic/channel args)
- `internal/util` → `internal/statsd` - statsd client & host key utilities
- `internal/util` → `internal/protocol` - protocol utilities (TCP server, errors, names validation, byte handling)
- `internal/util` → `internal/version` - version information
- `internal/util` → `internal/quantile` - quantile/percentile calculations
- `internal/util` → `internal/stringy` - string utilities (template functions, slice operations)

### External Dependencies
- Remove vendored `internal/semver` → use external `github.com/blang/semver`

### Updates
- Update all imports across apps (nsqd, nsqlookupd, nsqadmin, nsq_*, to_nsq, ...)
- Update lookupd types & utilities
- Update HTTP handlers, protocol handlers, stats, etc.

## Why
The `util` package had become a catch-all with mixed concerns. This reorganization:
- Improves code organization and discoverability
- Creates clear boundaries between different functional areas
- Makes dependencies more explicit
- Follows Go best practices for package structure