# Refactor: Migrate host/v5 metadata payload to component architecture

## Summary
Migrate the "host" metadata payload (previously named "v5") to the component-based architecture using FX dependency injection.

## Changes

### Component Migration
- Move host metadata generation from `pkg/metadata/v5` → `comp/metadata/host`
- Temporarily place shared utilities in `comp/metadata/host/utils` until full migration
- Implement `Component` interface with `GetPayloadAsJSON()` method
- Add Provider for metadata runner integration
- Add FlareProvider for flare bundle integration

### File Relocations
- `pkg/metadata/v5/*` → `comp/metadata/host/*`
- `pkg/metadata/host/*` → `comp/metadata/host/utils/*` (temporary)
- `pkg/metadata/common/*` → `comp/metadata/host/utils/common.go`
- Remove standalone `pkg/metadata/host.go` collector

### Dependency Injection
- Host metadata now injected via FX into:
  - Agent API server
  - Dogstatsd (with aggregator provisioning)
  - Run commands (all platforms)
- Add `provideAggregator()` helper for FX until full aggregator migration
- Resources component integration with optional disable support

### API Updates
- `api/internal/agent/agent.go`: Accept `host.Component` parameter
- `StartServer()`: Pass host metadata component through stack
- `metadataPayload()`: Use component's `GetPayloadAsJSON()` directly
- Remove direct `v5.GetPayload()` calls throughout codebase

### Configuration
- Move interval configuration handling to component initialization
- Validate collector intervals within component (min: 300s, max: 14400s)
- Remove host metadata from default scheduler collectors

### Utilities Consolidation
- Merge `common.GetPayload()` → `GetCommonPayload()`
- Standardize UUID retrieval across platforms
- Consolidate system stats collection
- Improve caching with typed cache keys

### Platform-Specific Changes
- **Windows**: Maintain existing WMI-based collection
- **Unix**: Maintain gopsutil-based collection  
- **Darwin**: Preserve Mac-specific version handling
- **Unsupported**: Stub implementations for FreeBSD/NetBSD/OpenBSD/Solaris

### Test Updates
- Update imports: `pkg/metadata/v5` → `comp/metadata/host`
- Update test assertions for component structure
- Mock component for dogstatsd tests
- Update process-agent status tests

### Breaking Changes (Internal)
- `v5.GetPayload()` removed - use `host.Component.GetPayloadAsJSON()`
- `host.InitHostMetadata()` removed - handled by component initialization
- Direct metadata collection removed from scheduler
- Logs status transport now uses getter/setter pattern

## Why
- Adopt modern component architecture for better dependency management
- Enable easier testing through dependency injection
- Prepare for full metadata subsystem migration
- Improve separation of concerns between collection and serialization
- Enable feature-specific component composition (e.g., dogstatsd without full metadata)

## Testing
- Verify v5 metadata payload unchanged on Windows/macOS/Linux
- Process agent status shows hostname correctly: `sudo -u dd-agent /opt/datadog-agent/embedded/bin/process-agent status`
- Agent status includes all expected metadata fields
- Dogstatsd metadata collection works independently