# Reorganize error hierarchy in `cli` package to inherit from `ApplicationError`

## Summary
Refactor error classes in the `cli` package to ensure all errors inherit from `ApplicationError` for normalized Sentry error reporting.

## Why
- Error classes scattered across codebase without consistent inheritance hierarchy
- Some errors don't properly inherit from `ApplicationError`
- Need to normalize error handling for better Sentry reporting
- Follow-up to #7820

## Changes

**Extract errors from `ResponseHelper.ts` to dedicated files:**
- Move `ResponseError` (abstract base) → `errors/response-errors/abstract/response.error.ts`
- Move HTTP error classes to `errors/response-errors/`:
  - `BadRequestError`, `AuthError`, `UnauthorizedError`, `NotFoundError`
  - `ConflictError`, `UnprocessableRequestError`
  - `InternalServerError`, `ServiceUnavailableError`

**Extract inline error classes to dedicated files in `errors/`:**
- `CredentialNotFoundError` (from `CredentialsHelper.ts`)
- `UnrecognizedNodeTypeError` (from `NodeTypes.ts`)
- `ExternalSecretsProviderNotFoundError` (from `ExternalSecrets.service.ee.ts`)
- `FeatureNotLicensedError` (from `License.ts`)
- `NotStringArrayError` (from `config/utils.ts`)
- `VariableCountLimitReachedError`, `VariableValidationError` (from `variables.service.ee.ts`)
- `InvalidRoleError`, `SharedWorkflowNotFoundError`, `WorkflowHistoryVersionNotFoundError`

**Update all imports across codebase** to use new error locations (~80+ files affected)

**Ensure all errors extend `ApplicationError`** from `n8n-workflow` package

## Outcome
- ✅ Consistent error hierarchy across `cli` package
- ✅ All errors properly inherit from `ApplicationError`
- ✅ Better organized error structure with dedicated files
- ✅ Normalized Sentry error reporting