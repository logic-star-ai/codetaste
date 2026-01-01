# Refactor Authentication SPI and Picketlink to use ProviderSession

## Summary

Refactor provider lifecycle management to support proper dependency injection and component dependencies. Remove `KeycloakRegistry` in favor of `ProviderSession`-based dependency resolution.

## Changes

### Provider Lifecycle
- Modified all `ProviderFactory.create()` methods to accept `ProviderSession` parameter
- Added proper `init()` and `close()` lifecycle method invocation
- Only call `close()` on providers that have been initialized

### Authentication SPI
- `AuthenticationProvider` now extends `Provider` interface
- Created `AuthenticationProviderFactory` for factory pattern
- `AuthenticationManager` constructor now requires `ProviderSession`
- Replaced ServiceLoader discovery with factory-based approach
- Updated META-INF/services from `AuthenticationProvider` → `AuthenticationProviderFactory`

### Picketlink Integration  
- Replaced `PartitionManagerProvider` with `IdentityManagerProvider`
- Created new module structure:
  - `keycloak-picketlink-api` - Provider interfaces
  - `keycloak-picketlink-realm` - Realm-based implementation
- Moved `PartitionManagerRegistry` to realm package
- `PicketlinkAuthenticationProvider` now receives `IdentityManagerProvider` via constructor injection

### Core Changes
- Moved `ProviderSession` and `ProviderSessionFactory` from services to core module
- Added `getAllProviders()` method to `ProviderSession` interface
- Removed `KeycloakRegistry` class entirely
- Store factories directly in `ServletContext` instead of registry

### Dependency Management
- Providers can now depend on other providers via `ProviderSession.getProvider()`
- ProviderSessionFactory properly manages component dependencies
- Added configuration for IdentityManagerProvider selection via `Config.getIdentityManagerProvider()`

## Why

- Enable proper dependency injection between providers
- Standardize lifecycle management across all provider types
- Remove ad-hoc registry pattern in favor of consistent factory pattern
- Support lazy initialization and proper cleanup
- Allow providers to access other providers during instantiation