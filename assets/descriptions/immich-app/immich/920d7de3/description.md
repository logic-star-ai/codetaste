# Refactor Enum Casing to PascalCase

## Summary
Convert all enum value casing from `SCREAMING_SNAKE_CASE` to `PascalCase` throughout the codebase for consistency with sync naming conventions and generated web API SDK.

## Why
- Match recent sync naming conventions
- Align with generated API SDK on web client
- Improve code consistency and readability
- Follow TypeScript/JavaScript PascalCase convention for enums

## Changes

### Enum Definitions (`enum.ts`)
- `ImmichWorker`: `API` → `Api`, `MICROSERVICES` → `Microservices`
- `ImmichCookie`: `ACCESS_TOKEN` → `AccessToken`, `AUTH_TYPE` → `AuthType`, ...
- `ImmichHeader`: `API_KEY` → `ApiKey`, `USER_TOKEN` → `UserToken`, ...
- `QueueName`: `BACKGROUND_TASK` → `BackgroundTask`, `SMART_SEARCH` → `SmartSearch`, ...
- `Permission`: `ALL` → `All`, `ACTIVITY_READ` → `ActivityRead`, ...
- `AssetType`: `IMAGE` → `Image`, `VIDEO` → `Video`, ...
- `LogLevel`: `LOG` → `Log`, `WARN` → `Warn`, `ERROR` → `Error`, ...
- `TranscodeHWAccel` → `TranscodeHardwareAcceleration`: `NVENC` → `Nvenc`, ...
- `SystemMetadataKey`: `ADMIN_ONBOARDING` → `AdminOnboarding`, ...
- `UserMetadataKey`: `PREFERENCES` → `Preferences`, `LICENSE` → `License`, ...
- `AssetPathType`: `ORIGINAL` → `Original`, `PREVIEW` → `Preview`, ...
- `JobName`: `USER_DELETION` → `UserDeletion`, `ASSET_DELETION` → `AssetDeletion`, ...
- ... and many more

### Affected Areas
- Controllers: All `@Authenticated` permission decorators
- Services: Job handlers, business logic
- Repositories: Database queries, metadata operations
- DTOs: Default values, validators
- Configuration: System config defaults
- Constants: Vector extensions, storage folders
- Tests: Fixtures, stubs, specs
- Storage: Path type handling
- Media: Codec configurations

## Impact
- **Breaking change** for API consumers relying on enum string values
- All enum usages updated across ~100+ files
- Config defaults updated (backward compatible via migration)
- No functional changes, purely cosmetic refactoring