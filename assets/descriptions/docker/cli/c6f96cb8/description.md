# Remove transport package abstraction

## Summary
Remove the `transport` package and its associated abstractions. Replace with direct use of `*http.Client` and a few helper functions. Eliminate the forked `ctxhttp` implementation (`transport/cancellable`) that was maintained solely for mocking purposes.

## Why
- The `transport` package doesn't provide significant value - it's an unnecessary abstraction layer
- Maintaining a fork of `ctxhttp` just to support an unnecessary mock is overhead
- The `transport.Client` interface and `transport.Sender` interface add complexity without clear benefits
- Direct use of `*http.Client` is clearer and more standard

## Changes
- Remove entire `transport/` package (including `cancellable/`, `client.go`, `transport.go`)
- Replace `transport.Client` with `*http.Client` in `Client` struct
- Replace `transport` field with `client` field in `Client`
- Add helper functions `resolveTLSConfig()` and `resolveScheme()` in new `transport.go`
- Use `golang.org/x/net/context/ctxhttp` directly instead of forked version
- Update `NewClient()` to configure `http.Transport` directly using `sockets.ConfigureTransport()`
- Simplify `newMockClient()` - remove unnecessary `tlsConfig` parameter
- Update all tests to use simplified mock client creation
- Update `hijack.go` to resolve TLS config from transport
- Update `request.go` to use `ctxhttp.Do()` and resolve scheme from transport

## Notes
- No breaking API changes
- Further refactoring of client interface may be beneficial (confusion between transport/http/application layers remains)
- All existing tests continue to pass with updated mocking approach