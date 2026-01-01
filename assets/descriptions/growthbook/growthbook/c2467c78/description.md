# Title
-----
Remove relative imports in back-end, use absolute imports

# Summary
-------
Replace all relative imports (`../`, `../../`) with absolute imports using `back-end/*` prefix throughout the entire back-end codebase.

Examples:
- `import ... from "../../types/organization"` → `import ... from "back-end/types/organization"`
- `import ... from "../models/UserModel"` → `import ... from "back-end/src/models/UserModel"`
- `import ... from "./validations"` → `import ... from "back-end/src/api/.../validations"`

# Why
---
**Canonical imports**: Imports become location-independent and only depend on the target file, not the importing file's location.

**Easier refactoring**:
- Moving imported files: fix all imports with single find/replace
- Moving importing files: imports remain valid automatically
- Splitting files: copy/paste imports without adjusting paths

**Improved readability**: Clear distinction between similar paths like `back-end/types` vs `back-end/src/types`. No more ambiguous `../types/...` imports.

# Implementation
---------------
- Update tsconfig.json: add `baseUrl` and `paths` configuration
- Update package.json: switch to `tspc`, add `ts-patch` + `typescript-transform-paths`
- Update ESLint config: add back-end paths to linting scope
- Update ~800+ import statements across:
  - `src/**/*.ts`
  - `types/**/*.ts`
  - `test/**/*.ts`
- Update README.md examples

# Scope
------
All `.ts` and `.tsx` files in:
- `/packages/back-end/src/**`
- `/packages/back-end/types/**`
- `/packages/back-end/test/**`