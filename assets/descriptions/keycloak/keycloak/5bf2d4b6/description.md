# Rename Legacy* Classes After Map Store Removal

## Summary
Remove `Legacy*` prefix from classes, interfaces, and configuration options that were renamed during Map Store development.

## Background
During Map Store development, several classes associated with the current store were renamed with a `Legacy*` prefix. Now that Map Store is being removed, these names need to be reverted.

## Classes/Interfaces to Rename

### Core Storage
- `LegacyDatastoreProvider` → `DefaultDatastoreProvider`
- `LegacyDatastoreProviderFactory` → `DefaultDatastoreProviderFactory`  
- `LegacyExportImportManager` → `DefaultExportImportManager`
- `LegacyMigrationManager` → `DefaultMigrationManager`
- `LegacyStoreManagers` → `StoreManagers`
- `LegacyRealmModel` → `StorageProviderRealmModel`

### Credentials & User Management
- `LegacyUserCredentialManager` → `UserCredentialManager`

### Quarkus-specific
- `LegacyJpaConnectionProviderFactory` → `QuarkusJpaConnectionProviderFactory`
- `LegacyInfinispanConnectionFactory` → `QuarkusInfinispanConnectionFactory`

### Events
- `LegacyStoreMigrateRepresentationEvent` → `StoreMigrateRepresentationEvent`
- `LegacyStoreSyncEvent` → `StoreSyncEvent`

## Configuration Options
Rename JPA provider configuration options:
- `spi-connections-jpa-legacy-initialize-empty` → `spi-connections-jpa-quarkus-initialize-empty`
- `spi-connections-jpa-legacy-migration-export` → `spi-connections-jpa-quarkus-migration-export`
- `spi-connections-jpa-legacy-migration-strategy` → `spi-connections-jpa-quarkus-migration-strategy`

## Test Infrastructure
- `@LegacyStore` annotation → `@Storage`
- CI job names: `legacy-store-integration-tests` → `store-integration-tests`
- Test profiles: `legacy-jpa*` → `jpa*`
- Test provider classes: `CustomLegacy*Provider` → `Custom*Provider`

## Documentation Updates
- Update migration guides
- Update server configuration guides
- Update upgrade notes for 24.0.0