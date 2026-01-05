# Refactor: Reorganize error hierarchy in `core` and `workflow` packages

## Summary

Reorganize error hierarchies in `core` and `workflow` packages to ensure all errors inherit from `ApplicationError` for normalized Sentry error reporting.

## Changes

### `core` package

- Rename `ReportableError` → `ApplicationError`
- Create abstract error base classes:
  - `FileSystemError` → `FileNotFoundError`, `DisallowedFilepathError`
  - `BinaryDataError` → `InvalidModeError`, `InvalidManagerError`
  - `InvalidExecutionMetadataError`
- Move errors to dedicated files in `/errors` directory
- Rename `WorkflowExecutionMetadata.ts` → `ExecutionMetadata.ts`

### `workflow` package

- Create abstract base classes:
  - `ExecutionBaseError` (extends `ApplicationError`)
  - `NodeError` (extends `ExecutionBaseError`)
- Reorganize error hierarchy:
  - `WorkflowActivationError` → `WorkflowDeactivationError`, `WebhookPathTakenError`
  - `WorkflowOperationError` → `SubworkflowOperationError` → `CliWorkflowOperationError`
  - `ExpressionError` → `ExpressionExtensionError`
  - `NodeError` → `NodeOperationError`, `NodeApiError`
  - `NodeSslError`
- Split monolithic `NodeErrors.ts` into separate error files
- Rename classes:
  - `WebhookPathAlreadyTakenError` → `WebhookPathTakenError`
  - `NodeSSLError` → `NodeSslError`
  - `UnknownManagerError` → `InvalidManagerError`
  - `InvalidPathError` → `DisallowedFilepathError`
  - `ExecutionMetadataValidationError` → `InvalidExecutionMetadataError`
- Update imports across codebase

## Implementation

- Move all error classes to `/errors` directory with proper structure
- Create `/errors/abstract` subdirectory for base classes
- Each error gets its own file
- Export all errors from `/errors/index.ts`
- Update `ErrorReporterProxy` to reference `ApplicationError`