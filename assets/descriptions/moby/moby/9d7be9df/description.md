# Remove transport package and simplify client architecture

## Summary
Remove `client/transport` package and replace with simpler helper functions. The transport abstraction doesn't provide real value and maintains an unnecessary ctxhttp fork for mocking.

## Why
- Transport package is over-engineered w/ minimal benefit
- Maintaining forked ctxhttp solely for unnecessary mock support
- Confusing separation between transport/HTTP/application layers
- Mocking achievable via simpler approach

## Changes

**Removal:**
- Delete entire `client/transport` package
- Remove forked ctxhttp implementation (`client/transport/cancellable/`)
- Remove `transport.Client` interface and implementations

**Replacement:**
- Use `*http.Client` directly in `Client` struct (replace `transport` field w/ `client`)
- Use upstream `golang.org/x/net/context/ctxhttp` directly
- Add `transport.go` w/ helper functions:
  - `resolveTLSConfig()` - extract TLS config from http.RoundTripper
  - `resolveScheme()` - determine http/https from transport
  - `transportFunc` - function type for test mocking

**Updates:**
- `NewClient()` - setup http.Transport directly if client is nil
- `client_mock_test.go` - `newMockClient()` returns `*http.Client` w/ custom RoundTripper
- All `*_test.go` files - update to use simpler mock client
- `hijack.go` - resolve TLS config via helper instead of `transport.TLSConfig()`
- `request.go` - use `ctxhttp.Do()` directly, resolve scheme via helper

## Benefits
- ✓ Simpler, more idiomatic Go
- ✓ Reduced maintenance (no forked deps)
- ✓ Clearer code structure
- ✓ **No breaking API changes**

## Notes
Client interface could use further refactoring - confusion remains between protocol/transport layers due to host/URL connection string model. Future: consider `NewClient(*http.Client)` approach.