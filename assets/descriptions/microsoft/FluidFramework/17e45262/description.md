# Move telemetry interfaces to core-interfaces

## Summary
Refactor to relocate telemetry-related interfaces and types from `@fluidframework/common-definitions` to `@fluidframework/core-interfaces` package.

## Interfaces/Types Moved
- `ILoggingError`
- `ITaggedTelemetryPropertyType`
- `ITelemetryBaseEvent`
- `ITelemetryBaseLogger`
- `ITelemetryErrorEvent`
- `ITelemetryGenericEvent`
- `ITelemetryLogger`
- `ITelemetryPerformanceEvent`
- `ITelemetryProperties`
- `TelemetryEventCategory`
- `TelemetryEventPropertyType`

## Changes
- Copy interface implementations from `common-definitions` to `core-interfaces`
- Update all imports across codebase: `@fluidframework/common-definitions` → `@fluidframework/core-interfaces`
- Deprecate old interfaces in `common-definitions` (marked with `@deprecated` tag)
- Update API reports for affected packages
- Update package dependencies where needed

## Why
Preparation for removing shared interfaces from `common-definitions` package. Telemetry interfaces belong in `core-interfaces` as foundational contracts.

## Scope
Affected packages include:
- Core: `container-definitions`, `datastore-definitions`, `driver-definitions`, `runtime-definitions`
- Drivers: `driver-utils`, `driver-web-cache`, `file-driver`, `local-driver`, `odsp-driver`, `replay-driver`, `routerlicious-driver`
- Loaders: `container-loader`, `location-redirection-utils`
- Runtime: `container-runtime`, `runtime-utils`
- Test utilities: `test-driver-definitions`, `test-utils`, `mocha-test-setup`
- Tools: `devtools-core`, `fluid-runner`, `replay-tool`, `telemetry-generator`
- Clients: `azure-client`, `tinylicious-client`
- ...and more