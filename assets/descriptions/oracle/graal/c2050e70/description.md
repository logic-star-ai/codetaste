# Title
Remove unnecessary SnippetReflectionProvider arguments and fields

## Summary
`SnippetReflectionProvider` has been accessible via `Providers.getSnippetReflection()` for quite some time, making separate parameters and fields redundant throughout the codebase. This refactoring eliminates unnecessary passing of `SnippetReflectionProvider` where it can be accessed through existing APIs.

## Why
- **Reduce boilerplate**: Many methods unnecessarily accept `SnippetReflectionProvider` as a parameter when they already have access to it via `Providers` or `GraphBuilderContext`
- **Simplify signatures**: Removing redundant parameters makes method signatures cleaner and easier to understand
- **Improve maintainability**: Fewer parameters to track and maintain across the codebase

## Changes

### Core Infrastructure
- Remove `snippetReflection` field from `ReplacementsImpl` (use `getProviders().getSnippetReflection()`)
- Remove `snippetReflection` parameter from `InternalFeature.registerInvocationPlugins(...)` 
- Remove `snippetReflection` parameter from `InternalFeature.registerGraalPhases(...)`
- Update `RuntimeConfiguration` to no longer store/expose `SnippetReflectionProvider`

### Replacements & Plugins
- `HotSpotReplacementsImpl`, `SubstrateReplacements`: Remove `snippetReflection` constructor parameter
- `InvocationPlugin` implementations: Use `b.getSnippetReflection()` instead of captured/field references
- `CInterfaceEnumTool`, `CInterfaceInvocationPlugin`: Remove `snippetReflection` field/parameter
- `InstrumentPhase`, `InstrumentationSuite`: Remove `snippetReflection` parameter

### Call Sites
- Update all `registerInvocationPlugins(...)` implementations
- Update all `registerGraalPhases(...)` implementations  
- Update `createReplacements(...)` calls to not pass `snippetReflection`
- Adjust test code using `ReplacementsImpl` or related APIs

### Access Pattern
Replace:
```java
snippetReflection.asObject(...)
```
With:
```java
b.getSnippetReflection().asObject(...)
// or
getProviders().getSnippetReflection().asObject(...)
```

## Note
This is a **mechanical refactoring** with **no functional changes**. Not every occurrence is addressed—only easily refactorable cases where alternative access exists.