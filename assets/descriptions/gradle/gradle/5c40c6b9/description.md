Title
-----
Replace `Factory<PatternSet>` with dedicated `PatternSetFactory` service

Summary
-------
Introduce a dedicated internal service `PatternSetFactory` to replace all usages of the generic `Factory<PatternSet>` type throughout the codebase.

- Create `PatternSetFactory` interface with `createPatternSet()` method
- Add `DefaultPatternSetFactory` implementation
- Replace all `Factory<PatternSet>` parameters/fields/... with `PatternSetFactory`
- Update all `factory.create()` calls to `factory.createPatternSet()`
- Remove generic `ServiceRegistry.getFactory()` calls where applicable

Why
---
**Navigation**: Generic `Factory<PatternSet>` type makes it difficult to find usages during development. A dedicated named type improves code navigation and discoverability.

**Service Management**: `PatternSetFactory` is one of few users of `ServiceRegistry.getFactory()` functionality. Removing this dependency simplifies service registry implementation and opens opportunity to remove/repurpose `getFactory()` altogether.

Scope
-----
Files affected across multiple modules:
- `platforms/core-configuration/...` (configuration-cache, core-serialization-codecs, file-collections, file-operations)
- `platforms/jvm/testing-jvm/...`
- `subprojects/core/...`
- `subprojects/core-api/...` (new factory interface/impl)

Implementation
--------------
1. Create `PatternSetFactory` interface in `org.gradle.api.tasks.util.internal`
2. Create `DefaultPatternSetFactory` implementation
3. Register service in scope services (Global, BuildTree, Project, ...)
4. Replace all occurrences of `Factory<PatternSet>` → `PatternSetFactory`
5. Replace all `create()` → `createPatternSet()` calls
6. Update `PatternSets` utility class
7. Remove generic factory methods from codecs where no longer needed