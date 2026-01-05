# Refactor x2cpg configuration to use dependent types

## Summary
Replace generic type parameters with dependent types in `X2CpgFrontend` and eliminate the error-prone `withInheritedFields()` pattern from all frontend config classes.

## Why
- `withInheritedFields()` is a footgun requiring manual implementation in each frontend config
- Generic type parameters (`X2CpgFrontend[T]`) lead to verbose code with type casts
- Inconsistent mutability: some `with*` methods mutated, others returned copies

## Changes

### Type System
- Replace `X2CpgFrontend[T <: X2CpgConfig[T]]` with dependent type member: `type ConfigType <: X2CpgConfig[ConfigType]`
- Each frontend defines `val defaultConfig: ConfigType`

### Config Structure
- Extract common fields into `X2CpgConfig.GenericConfig` case class member
- Configs now have `genericConfig: X2CpgConfig.GenericConfig` instead of inheriting fields
- Add `withGenericConfig(value: GenericConfig): ConfigType` method
- Remove all `withInheritedFields(this)` calls from `with*` methods

### Immutability
- All `with*` methods now return copies (case class `.copy()`)
- Consistent immutable pattern across all frontends

### X2CpgMain
- Add default `run()` implementation handling server mode
- Constructor now `X2CpgMain(frontend, cmdLineParser)` instead of `X2CpgMain(cmdLineParser, frontend)`
- HTTP server refactored to `server` member variable

### AstGen
- Rename `AstGenConfig` trait → consolidated into base config
- Rename `AstGenRunnerBase` → `AstGenRunner`
- Make `AstGenProgramMetaData` abstract class instead of case class

## Affected Frontends
c2cpg, csharpsrc2cpg, ghidra2cpg, gosrc2cpg, javasrc2cpg, jimple2cpg, jssrc2cpg, kotlin2cpg, php2cpg, pysrc2cpg, rubysrc2cpg, swiftsrc2cpg