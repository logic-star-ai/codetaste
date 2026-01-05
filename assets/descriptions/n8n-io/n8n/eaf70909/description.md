# Title
Enforce consistent type imports across FE packages

# Summary
Integrate `@typescript-eslint/consistent-type-imports` ESLint rule into the base config and apply lintfixes across all frontend packages to enforce consistent TypeScript type import syntax.

# Why
- Improve code consistency by using explicit `type` keyword for type-only imports
- Better code clarity by distinguishing type imports from value imports
- Enable better tree-shaking and build optimization by making type imports explicit
- Centralize ESLint rule configuration in base config instead of per-package overrides

# Changes
**ESLint Configuration:**
- Move `@typescript-eslint/consistent-type-imports` rule to base config (`packages/@n8n_io/eslint-config/base.js`)
- Remove rule from individual package configs (`cli`, `core`, `node-dev`, `nodes-base`, `workflow`)

**Code Updates:**
- Update all FE packages (`design-system`, `editor-ui`, etc.) to use consistent type imports
- Convert `import { Type }` → `import type { Type }` for type-only imports
- Split mixed imports into separate type and value imports where needed
- Apply across Vue components, TypeScript files, stores, composables, utils, etc.

# Scope
- `packages/@n8n_io/eslint-config/`
- `packages/design-system/`
- `packages/editor-ui/`
- `packages/cli/`, `packages/core/`, `packages/node-dev/`, `packages/nodes-base/`, `packages/workflow/` (config only)

# Technical Details
Pattern transformation:
```typescript
// Before
import { IUser, someFunction } from '@/module';

// After  
import type { IUser } from '@/module';
import { someFunction } from '@/module';
```