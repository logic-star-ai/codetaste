# Rename audit to events

## Summary
Rename all "audit" references to "events" throughout the codebase for better terminology and clarity.

## Changes

### Core Refactoring
- **Packages**: `org.keycloak.audit.*` → `org.keycloak.events.*`
- **Directories**: `audit/` → `events/`
- **Artifacts**: `keycloak-audit-*` → `keycloak-events-*`

### API Classes
- `AuditProvider` → `EventStoreProvider`
- `AuditListener` → `EventListenerProvider`
- `Audit` → `EventBuilder`
- `AuditManager` → `EventsManager`
- `AuditProviderFactory` → `EventStoreProviderFactory`
- `AuditListenerFactory` → `EventListenerProviderFactory`

### Data Model
- Event field: `event` → `type` (with corresponding getters/setters)
- Realm fields: `auditEnabled` → `eventsEnabled`, `auditExpiration` → `eventsExpiration`, `auditListeners` → `eventsListeners`
- Database columns: `EVENT` → `TYPE`, `AUDIT_ENABLED` → `EVENTS_ENABLED`, etc.
- Tables: `REALM_AUDIT_LISTENERS` → `REALM_EVENTS_LISTENERS`

### Configuration
- SPI names: `audit` → `eventsStore`, `audit-listener` → `eventsListener`
- Admin roles: `VIEW_AUDIT` → `VIEW_EVENTS`, `MANAGE_AUDIT` → `MANAGE_EVENTS`

### UI & REST
- Admin console routes: `/audit` → `/events`, `/audit-settings` → `/events-settings`
- REST endpoints: `/admin/realms/{realm}/audit` → `/admin/realms/{realm}/events`
- Query parameters: `event` → `type`

### Implementations
- JPA: `JpaAuditProvider` → `JpaEventStoreProvider`, `EventEntity` updates
- Mongo: `MongoAuditProvider` → `MongoEventStoreProvider`
- Email: `EmailAuditListener` → `EmailEventListenerProvider`
- Logging: `JBossLoggingAuditListener` → `JBossLoggingEventListenerProvider`

### Documentation
- `modules/audit.xml` → `modules/events.xml`
- README files updated
- All references in docbook and examples updated

## Why
- **Better terminology**: "Events" more accurately describes user-related actions (login, register, etc.) than "audit"
- **Clearer separation**: Distinguish between event store (persistence) and event listeners (reactions)
- **Improved API**: `EventBuilder` is more intuitive than `Audit` for constructing events