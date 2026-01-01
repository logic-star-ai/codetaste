# Remove Rome Formatter - Complete Migration to Biome

## Summary
Remove all Rome formatter code and complete the transition to Biome. Rome had a political rename to Biome, and we've had deprecated Rome support alongside Biome for compatibility. Time to clean house and remove the legacy Rome code entirely.

## Why
- Rome project was forked/renamed to Biome
- Maintaining parallel Rome/Biome code paths adds unnecessary complexity
- All Rome functionality is available in Biome
- Users have had time to migrate (deprecation warnings in place)

## What's Being Removed
- `com.diffplug.spotless.rome.*` package → `com.diffplug.spotless.biome.*`
- `RomeStep` → `BiomeStep`
- `RomeExecutableDownloader` → `BiomeExecutableDownloader`
- `BiomeFlavor.ROME` enum variant
- All Rome-specific config classes:
  - Gradle: `RomeGeneric`, `RomeJs`, `RomeJson`, `RomeTs`
  - Maven: `Rome`, `RomeJs`, `RomeJson`, `RomeTs`
- Rome-specific methods: `rome()`, `addRome()`, etc.
- Rome test files and integration tests
- Rome test resources (`testlib/.../rome/...`)

## Breaking Changes
- **BREAKING**: `rome()` / `addRome()` methods removed - use `biome()` / `addBiome()`
- **BREAKING**: `BiomeFlavor.ROME` removed - use `BiomeFlavor.BIOME`
- **BREAKING**: Rome package/classes no longer exist

## Migration Path
Users should update their configs:
- Change `rome { ... }` → `biome { ... }`
- Change `rome.json` → `biome.json`
- Update version to Biome versions (1.2.0+)