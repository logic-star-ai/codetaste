# Refactor enum imports to use `@calcom/prisma/enums`

## Summary
Replace enum imports from `@prisma/client` and `@calcom/prisma/client` with `@calcom/prisma/enums` across the codebase.

## Why
**Performance**: Importing enums from `@prisma/client` bundles ~28MB of Prisma client code. Using `@calcom/prisma/enums` reduces this to ~0.1KB per import.

## Scope
Update imports for all Prisma enums:
- `MembershipRole`
- `CreationSource`
- `SchedulingType`
- `BookingStatus`
- `RedirectType`
- `IdentityProvider`
- `SMSLockState`
- `AttributeType`
- `WebhookTriggerEvents`
- `WorkflowActions`, `WorkflowTemplates`
- `TimeUnit`, `PeriodType`
- `UserPermissionRole`
- `PhoneNumberSubscriptionStatus`
- `RRResetInterval`, `RRTimestampBasis`
- ...

## Changes
- API v1/v2 endpoints
- Web app pages & components
- E2E tests
- TRPC routers
- App store packages
- Feature packages
- Lib utilities

## Impact
Significant bundle size reduction from avoiding unnecessary Prisma client imports where only enum types are needed.