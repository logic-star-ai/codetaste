# Title
Consolidate public API exports to `angular2/core`

# Summary
Refactor public API structure to export core APIs from `angular2/core` instead of multiple fragmented modules.

# Why
- Simplify import paths... developers should import from a single entry point
- Reduce confusion about where to import common types/decorators/utilities
- Better align with framework conventions and improve developer experience

# Changes
- **Consolidated exports**: Move APIs from `angular2/{forms,di,directives,change_detection,bootstrap,render,metadata,debug,pipes}` to `angular2/core`
- **Auto-inject FORM_BINDINGS**: Automatically add FORM_BINDINGS to application root injector
- **New barrel files**: Create internal barrel files (`src/core/{compiler,services,zone,util,facade}.ts`) for better organization
- **Bootstrap changes**: `angular2/bootstrap.ts` now only for Dart apps + internal examples; JS users import from `angular2/core`

# Breaking Changes
**All affected exports now imported from `angular2/core`**:
- `angular2/forms` → `angular2/core`
- `angular2/di` → `angular2/core`
- `angular2/directives` → `angular2/core`
- `angular2/change_detection` → `angular2/core`
- `angular2/bootstrap` (except Dart) → `angular2/core`
- `angular2/render` → `angular2/core`
- `angular2/metadata` → `angular2/core`
- `angular2/debug` → `angular2/core`
- `angular2/pipes` → `angular2/core`

# Migration
Update imports throughout codebase:
```ts
// Before
import {Component} from 'angular2/metadata';
import {NgFor, NgIf} from 'angular2/directives';
import {Injector} from 'angular2/di';

// After
import {Component, NgFor, NgIf, Injector} from 'angular2/core';
```

Closes #3977