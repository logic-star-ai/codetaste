# Lazy-load all AWS API clients

## Summary

Refactored AWS SDK client initialization to use lazy loading instead of eagerly creating all 300+ service clients during provider configuration. Clients are now created on-demand and cached in maps, reducing memory footprint and initialization time.

## Changes

**Architecture**
- Replaced 300+ individual client fields in `AWSClient` with two maps (`clients`, `conns`) protected by `sync.Mutex`
- Added generic `conn[T]()` and `client[T]()` helper functions for lazy initialization pattern
- Each service package now implements `NewConn()`/`NewClient()` factory methods

**Service Package Interface**
- Added `config map[string]any` field to each `servicePackage` struct
- Implemented `Configure(ctx, config)` method to receive provider configuration
- Moved client creation logic from `internal/conns` → individual service packages via:
  - `NewConn(ctx)` for AWS SDK Go v1 clients
  - `NewClient(ctx)` for AWS SDK Go v2 clients
  - Optional `CustomizeConn(ctx, client)` for service-specific retry/error handling

**Custom Client Creation**
- Services requiring non-standard initialization (e.g., global services like Route53, Shield) now implement custom `NewConn()`/`NewClient()` methods
- Examples: `globalaccelerator`, `route53`, `shield`, `route53domains` force specific regions

**Client Customization**
- Moved retry logic customization from `internal/conns` to service packages
- Services with custom behavior: `chime`, `organizations`, `securityhub`, `ssoadmin`, `storagegateway`, `wafv2`, `s3`

**Code Generation**
- Updated `internal/generate/servicepackage` templates to generate `service_package_gen.go` files
- Generated `Configure()`, `NewConn()`, `NewClient()` methods for all services

## Why

- **Memory Efficiency**: Only instantiate clients actually used in practitioner configurations
- **Faster Startup**: Avoid creating 300+ clients upfront (many never used)
- **Maintainability**: Single initialization mechanism vs. dual (eager + lazy)
- **Separation of Concerns**: Service packages own their client lifecycle

## Implementation Notes

- Accessor methods like `meta.EC2Conn(ctx)` unchanged → zero resource implementation changes
- Custom client creation isolated to services with special requirements (regional forcing, custom endpoints)
- All client customization (retry handlers, etc.) encapsulated in service packages
- Backward compatible with existing resource/data source implementations

## Related

Closes #26626  
Relates #25602