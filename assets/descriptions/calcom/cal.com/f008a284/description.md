# Rename DWD to DelegationCredential

## Summary
Comprehensive codebase refactoring to rename "DWD" (Domain Wide Delegation) to "DelegationCredential" across all layers - database, backend, frontend, APIs, and translations.

## Why
- **Clarify terminology**: "Domain Wide Delegation" is Google-specific jargon
- **Generalize naming**: Better reflect broader applicability across workspace platforms (Google, Microsoft, etc.)
- **Improve maintainability**: More intuitive naming for future developers

## What Changed

### Database Schema
- New `DelegationCredential` table added with relations to:
  - `WorkspacePlatform` (via `workspacePlatformId`)
  - `Team`/Organization (via `organizationId`) 
  - `SelectedCalendar`, `DestinationCalendar`, `BookingReference`
- Field renames: `domainWideDelegationCredentialId` → `delegationCredentialId`
- Migration: `20250305114246_delegation_credentials_schema`

### Backend
- **Repositories**: `DomainWideDelegationRepository` → `DelegationCredentialRepository`
- **Files**: `packages/lib/server/repository/domainWideDelegation.ts` → `.../delegationCredential.ts`
- **Functions**: 
  - `getAllDwdCredentialsForUser` → `getAllDelegationCredentialsForUser`
  - `enrichHostsWithDwdCredentials` → `enrichHostsWithDelegationCredentials`
  - `buildNonDwdCredentials` → `buildNonDelegationCredentials`
  - `isDwdCredential` → `isDelegationCredential`
  - ...and many more

### API/TRPC
- **Router**: `domainWideDelegationRouter` → `delegationCredentialRouter`
- **Endpoints**: `/api/trpc/domainWideDelegation/*` → `/api/trpc/delegationCredential/*`
- **Handlers**: `add.handler`, `update.handler`, `toggleEnabled.handler`, etc. all renamed
- **Feature flag**: `domain-wide-delegation` → `delegation-credential`

### Frontend
- **Settings route**: `/settings/organizations/domain-wide-delegation` → `.../delegation-credential`
- **Page component**: `DomainWideDelegationList` → `DelegationCredentialList`
- **Hooks/Components**: All DWD references updated to DelegationCredential

### Translations
- Translation keys updated across **all locale files** (ar, az, bg, ca, cs, da, de, el, en, es, ...):
  - `domain_wide_delegation` → `delegation_credential`
  - `domain_wide_delegation_description` → `delegation_credential_description`
  - `add_domain_wide_delegation` → `add_delegation_credential`
  - ...etc.

### Types
- `DomainWideDelegation` → `DelegationCredential`
- `DomainWideDelegationWithSensitiveServiceAccountKey` → `DelegationCredentialWithSensitiveServiceAccountKey`
- Updated across Calendar, EventManager, App type definitions

### Tests
- Test files renamed and updated
- Mock functions: `createDwdCredential` → `createDelegationCredential`

## Scope
- **~200+ files** modified across:
  - `apps/api/v1`, `apps/api/v2`, `apps/web`
  - `packages/lib`, `packages/trpc`, `packages/prisma`
  - `packages/platform`, `packages/types`
  - All locale translation files

## Notes
- **Backward compatibility**: Old `DomainWideDelegation` schema remains in database (not removed)
- **Breaking change**: API endpoints and frontend routes changed
- Comments updated: "DWD" → "DelegationCredential" throughout code