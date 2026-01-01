# Title
-----
Introduce `vtenv` package to consolidate collation, parser & MySQL version dependencies

# Summary
-------
Introduces `vtenv.Environment` struct to wrap collation environment, SQL parser, and MySQL version into a single dependency object, replacing 3-parameter signatures across the codebase.

# Why
---
Many components were taking 3 separate parameters: `collationEnv *collations.Environment`, `parser *sqlparser.Parser`, and `mysqlVersion string`. This creates:
- Verbose function signatures
- Repetitive parameter passing
- Difficult future extensibility

# Changes
---
- **New Package**: `go/vt/vtenv/` with `Environment` struct wrapping:
  - `*collations.Environment`
  - `*sqlparser.Parser` 
  - MySQL version string
  - Truncate UI/Error length configs

- **Factory Methods**:
  - `vtenv.New(vtenv.Options{...})` - production initialization
  - `vtenv.NewTestEnv()` - test initialization

- **Signature Updates**: Functions now take `env *vtenv.Environment` instead of 3 params:
  - `NewTabletServer(..., env, ...)`
  - `NewVtctldServer(env, ...)`
  - `NewAPI(env, ...)`
  - `wrangler.New(env, ...)`
  - `...Init(..., env, ...)`

- **Entry Points**: All `main.go` files updated to initialize `vtenv` early

- **Accessors**: Components use `env.Parser()`, `env.CollationEnv()`, `env.Environment()`

# Benefits
---
- Reduced parameter count (3→1)
- Cleaner abstraction for environment state
- Easier to add future environment dependencies
- More consistent initialization patterns
- Simpler test setup with `NewTestEnv()`

# Related
---
Part of #14717 (refactoring to pass explicit state)