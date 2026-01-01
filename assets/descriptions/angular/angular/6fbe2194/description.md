# Title
-----
Refactor: Break circular dependencies in `@angular/core` by extracting symbols to dedicated files

# Summary
-------
Clean up circular dependencies in the core package by extracting symbols into separate, focused files. This reduces ~8 circular dependency chains tracked in the golden file.

# Why
---
Circular dependencies make code harder to understand, can cause subtle runtime issues, and complicate the module dependency graph.

# What Changed
--------------
**New files created to break circular dependencies:**

- `render3/definition_factory.ts` - extracted `FactoryFn` type + `getFactoryDef()` from `definition.ts`
- `render3/errors_di.ts` - extracted DI-specific errors (`throwCyclicDependencyError`, `throwProviderNotFoundError`, etc.) from `errors.ts`
- `render/api_flags.ts` - extracted `RendererType2` + `RendererStyleFlags2` from `render/api.ts`
- `render3/interfaces/renderer_dom.ts` - extracted DOM types (`RNode`, `RElement`, `RText`, `RComment`, `RCssStyleDeclaration`, etc.) from `renderer.ts`
- `render3/util/stringify_utils.ts` - extracted `renderStringify()` + `stringifyForError()` from `misc_utils.ts`
- `view/types.ts` - extracted `DebugContext` type from `view/index.ts`

**Import updates:**

- ~50+ files updated to import from new locations
- Changed barrel imports to specific module imports (e.g., `metadata/view`, `metadata/schema`, `di/metadata`, `di/interface/provider`)
- Updated test files to match new import paths

**Circular dependencies removed:**

- `application_ref.ts` ↔ `metadata.ts` ↔ `linker/compiler.ts` cycle
- Multiple `core.ts` ↔ `di.ts` ↔ `render3/...` cycles
- `debug_node.ts` ↔ `view/...` cycles
- `render/api.ts` ↔ `render3/interfaces/...` cycles (9 variations removed)
- `di/injector*.ts` circular chains (4 cycles removed)

# Impact
--------
- 8 circular dependency chains eliminated (tracked in `goldens/circular-deps/packages.json`)
- No functional changes, purely structural refactoring
- More explicit dependency graph, easier to understand code organization