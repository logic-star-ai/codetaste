# Refactor: Simplify Service Dependency Management

## Summary

Consolidate service dependencies by introducing a `BaseService` class that provides all repositories to services, eliminating repetitive constructor injection boilerplate.

## Why

- Reduce boilerplate code across ~30+ service classes
- Eliminate repetitive `@Inject` decorators and constructor parameters
- Simplify service instantiation in tests via unified `newTestService` utility
- Make repository access consistent across all services

## What Changed

**BaseService**
- Now injects all ~35 repositories via constructor
- Provides protected repository properties to extending services
- Auto-initializes `storageCore` and sets logger context
- Services simply extend `BaseService` instead of managing dependencies

**Service Classes**
- Removed explicit constructor dependency injection
- Changed from standalone classes to `BaseService` extensions
- Access repositories via inherited protected properties (e.g., `this.accessRepository`, `this.assetRepository`, ...)
- No more `@Inject` decorators or interface imports for repositories

**Test Utilities**
- Added `newTestService<T>()` helper function in `test/utils.ts`
- Instantiates all repository mocks once
- Returns `{ sut, ...mocks }` destructurable object
- Replaces per-test mock initialization boilerplate

**Test Files**
- Simplified from 10-20 lines of mock setup → single `newTestService()` call
- Destructure only needed mocks: `({ sut, assetMock, userMock } = newTestService(MyService))`

## Example

**Before:**
```ts
constructor(
  @Inject(IAccessRepository) private access: IAccessRepository,
  @Inject(IAssetRepository) private assetRepository: IAssetRepository,
  // ... 5-10 more dependencies
) {
  this.logger.setContext(MyService.name);
}
```

**After:**
```ts
export class MyService extends BaseService {
  // Repositories available via this.assetRepository, this.accessRepository, etc.
}
```

## Impact

- ~30+ services refactored
- ~30+ test files simplified
- All repository access patterns remain unchanged
- No breaking changes to service APIs