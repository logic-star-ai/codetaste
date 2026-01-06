# Replace `Factory<PatternSet>` with dedicated `PatternSetFactory` service

Introduce a dedicated internal service `PatternSetFactory` to replace all usages of the generic `Factory<PatternSet>` type throughout the codebase.

- Create `PatternSetFactory` interface with `createPatternSet()` method
- Add `DefaultPatternSetFactory` implementation
- Replace all `Factory<PatternSet>` parameters/fields/... with `PatternSetFactory`
- Update all `factory.create()` calls to `factory.createPatternSet()`
- Remove generic `ServiceRegistry.getFactory()` calls where applicable