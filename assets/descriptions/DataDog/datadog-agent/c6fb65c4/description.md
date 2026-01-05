Title
-----
Migrate components to new file hierarchy: `host`, `languagedetection/client`, and `process/forwarders`

Summary
-------
Restructure three components to follow new file hierarchy pattern where interface definitions remain in parent package while implementations move to dedicated `*impl/` subdirectories.

Components affected:
- `comp/metadata/host` → `comp/metadata/host/hostimpl`
- `comp/languagedetection/client` → `comp/languagedetection/client/clientimpl`
- `comp/process/forwarders` → `comp/process/forwarders/forwardersimpl`

Details
-------

### File Movement Pattern

For each component:
- **Keep** `component.go` with interface definition in parent package (`comp/.../component.go`)
- **Move** implementation files to `*impl/` subdirectory (`comp/.../componentimpl/*.go`)
- **Move** `Module()` function from `component.go` to implementation package
- **Move** utils subdirectories under impl package (e.g., `host/utils` → `hostimpl/utils`)

### Specific Changes

**comp/metadata/host**
- Move `host.go`, `payload*.go` → `hostimpl/`
- Move `utils/*` → `hostimpl/utils/`
- Remove `Module()` from `component.go`, add to `hostimpl/host.go`

**comp/languagedetection/client**
- Move `client.go`, `telemetry.go`, `util.go`, `client_test.go` → `clientimpl/`
- Module definition moves to `clientimpl/client.go`
- Update bundle to use `clientimpl.Module()`

**comp/process/forwarders**
- Move `forwarders.go` → `forwardersimpl/`
- Separate mock into `forwardersimpl/forwarders_mock.go` with build tag `//go:build test`
- Both `Module()` and `MockModule()` now in impl package

### Import Updates

Update all imports across codebase:
- cmd/agent, cmd/dogstatsd, cmd/process-agent commands
- Bundle definitions
- Test files
- Various pkg/ utilities (status, metadata, logs, etc.)

### Tasks Checklist

- Update exception list in `tasks/components.py` (remove migrated components)
- Ensure all tests pass with new import paths
- Verify bundle configurations use impl modules correctly