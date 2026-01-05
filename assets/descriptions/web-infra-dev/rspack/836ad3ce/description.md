# Title

Rename "harmony" terminology to "ESM" in Rust codebase

# Summary

Replace internal "harmony" naming throughout Rust code with "ESM" (ECMAScript Modules) terminology for improved code clarity and maintainability.

# Why

"Harmony" is webpack's legacy internal codename for ES modules that's confusing for developers unfamiliar with webpack's history. "ESM" is the standard, widely-understood term for ECMAScript Modules.

# Scope

**Core Changes:**
- Dependency structs: `Harmony*Dependency` → `ESM*Dependency`
  - `HarmonyImportSpecifierDependency` → `ESMImportSpecifierDependency`
  - `HarmonyExportImportedSpecifierDependency` → `ESMExportImportedSpecifierDependency`
  - `HarmonyCompatibilityDependency` → `ESMCompatibilityDependency`
  - ... (all harmony dependency variants)

- File names: `harmony_*.rs` → `esm_*.rs`
  - `harmony_import_dependency.rs` → `esm_import_dependency.rs`
  - `harmony_export_*.rs` → `esm_export_*.rs`
  - ...

- Runtime modules:
  - `HarmonyModuleDecoratorRuntimeModule` → `ESMModuleDecoratorRuntimeModule`
  - `HARMONY_MODULE_DECORATOR` → `ESM_MODULE_DECORATOR`

- Build metadata fields:
  - `strict_harmony_module` → `strict_esm_module`
  - `harmony_named_exports` → `esm_named_exports`

- Init fragment keys/stages:
  - `HarmonyImport` → `ESMImport`
  - `HarmonyExports` → `ESMExports`
  - `StageHarmonyImports` → `StageESMImports`
  - ...

- Functions and variables:
  - `harmony_import_dependency_apply` → `esm_import_dependency_apply`
  - `is_harmony_dep_like` → `is_esm_dep_like`
  - `last_harmony_import_order` → `last_esm_import_order`
  - ...

**Comments & Documentation:**
- Update comments referencing "harmony" → "ESM" or "ES modules"
- Update error message titles: `HarmonyLinkingError` → `ESModulesLinkingError`
- Update test descriptions and assertions

# Non-Goals

- ❌ No public API changes
- ❌ No user-facing breaking changes
- ❌ No functional behavior changes