# Refactor: use 'any' instead of 'interface{}' for consistency

Replace all occurrences of `interface{}` with `any` throughout the codebase (excluding generated files). Enable `revive.use-any` linter rule to enforce this convention going forward.