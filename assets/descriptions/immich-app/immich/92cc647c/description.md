# Title

Consolidate decorators, configuration, and validation logic into dedicated modules

# Summary

Reorganize scattered utility functions, decorators, validation logic, and configuration across the codebase into three centralized modules: `src/decorators.ts`, `src/validation.ts`, and `src/utils.ts`. Move app configuration to `src/config.ts`.

# Why

The codebase had utility functions, decorators, and validation logic scattered across multiple files (`domain.util.ts`, `infra.util.ts`, `infra.utils.ts`, `api-v1/validation/*`, `microservices/utils/*`), making them hard to locate and maintain.

# What Changed

**Created new consolidated modules:**
- `src/config.ts` - App configuration (from `domain.config.ts` + `infra.config.ts`)
- `src/decorators.ts` - Decorators (`Chunked*`, `DecorateAll`, `GenerateSql`, etc.)
- `src/validation.ts` - Validators, validation decorators, DTOs (`ValidateUUID`, `ValidateDate`, `ValidateBoolean`, `Optional`, `ParseMeUUIDPipe`, `FileNotEmptyValidator`, `UUIDParamDto`, etc.)
- `src/utils.ts` - Utility functions (file operations, number/coordinate parsing, Set operations, pagination helpers, cache control, etc.)

**Removed scattered files:**
- `domain/domain.config.ts`
- `domain/domain.util.ts`
- `infra/infra.util.ts`
- `api-v1/validation/*.ts`
- `microservices/utils/numbers.ts`
- `microservices/utils/exif/coordinates.ts`
- `controllers/dto/uuid-param.dto.ts`

**Updated imports throughout codebase** to reference new module locations.