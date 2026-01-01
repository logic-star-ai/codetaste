# Refactor: Consolidate `netio` into `hap` package and move public API to root

## Summary
Reorganize package structure by moving all `netio` files into `hap` package and promoting public API files from `hap` to root `hc` package.

## Why
- `netio` package name doesn't clearly convey HAP protocol implementation
- Public API (Config, Transport, etc.) should be at root level for easier imports
- Better separation between internal HAP protocol details and public interface
- Clearer package boundaries and responsibilities

## Changes

### netio → hap
- Move all `netio/*.go` files to `hap/` package
  - `connection.go`, `context.go`, `device.go`, `handler.go`, `session.go`, `secured_device.go`
  - `chunked_writer.go`, `constants.go`, `notification.go`
  - Subpackages: `controller/`, `data/`, `endpoint/`, `pair/`
- Rename types:
  - `HAPConnection` → `Connection`
  - `HAPContext` → `Context` + `Store` interface
  - `HAPTCPListener` → `TCPListener`
  - `New()` → `NewNotification()`
- Delete `netio/server.go` (consolidated into `hap/http/server.go`)

### hap → root (hc)
- Move public API files to root package:
  - `config.go`, `ip_transport.go`, `mdns.go`, `password.go`, `termination.go`, `transport.go`
  - Change package from `hap` to `hc`

### Other
- Move `netio/mac.go` → `util/mac.go`
- Update all imports throughout codebase
- Update README.md and examples

## Breaking Changes
- Import path changes: `hap.NewIPTransport` → `hc.NewIPTransport`
- Import path changes: `netio.*` → `hap.*`