Title
-----
Restructure :build-cache subproject for reuse outside Gradle

Summary
-------
Reorganize build cache modules to enable reuse outside of Gradle by:
- Extracting public API to `:build-cache-spi`
- Moving local cache implementation to `:build-cache-local`
- Breaking dependencies on Gradle-specific types

Why
---
Current structure couples build cache implementation to Gradle internals, preventing reuse in other contexts. This restructuring:
- Separates SPI from implementation
- Removes Gradle-specific type dependencies where possible
- Creates cleaner module boundaries

Changes
-------

**New subprojects:**
- `:build-cache-spi` - Public API for implementing build cache services
  - Move `BuildCacheEntryReader`, `BuildCacheEntryWriter`, `BuildCacheException`, `BuildCacheKey`, `BuildCacheService` from `:core-api`
  - `BuildCacheException` now extends `RuntimeException` instead of `GradleException`
  - `BuildCacheKey` no longer implements `Describable`; `getDisplayName()` deprecated → use `getHashCode()`

- `:build-cache-local` - Local build cache implementation
  - Move `DirectoryBuildCache*`, `H2BuildCacheService`, `LocalBuildCache` from `:build-cache`
  - Move related tests/integration tests

**Dependency restructuring:**
- `:build-cache-http` → depends only on `:build-cache-spi` + `:core-api` (not `:build-cache`)
- `:build-cache-base` → depends on `:build-cache-spi`
- `:build-cache` → cleaner dependencies after extracting local cache code

**Internal refactorings:**
- Introduce `BuildCacheKeyInternal` interface for internal HashCode access
- Move `DefaultBuildCacheKey` to `:execution` subproject
- Create `TestBuildCacheKey` in testFixtures
- Replace `TemporaryFileProvider` with `TemporaryFileFactory` interface
- Change `LocalBuildCacheService.loadLocally()`: `Action<File>` → `Consumer<File>`
- Remove `BuildCacheController.isEmitDebugLogging()`, pass as parameter instead
- Move `RootBuildCacheControllerRef` to `:core` (`.impl` package)

**Binary compatibility:**
- Breaking: `BuildCacheException` superclass changed
- Breaking: `BuildCacheKey.getDisplayName()` deprecated (unlikely to affect third-party implementations)