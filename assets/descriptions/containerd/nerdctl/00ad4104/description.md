# Title
Refactor test framework: reorganize into `mod/tigron` with sub-packages

# Summary
Reorganize the test framework module from `pkg/testutil/test` to `mod/tigron` and split it into logical sub-packages (`expect`, `require`, `test`) for better organization and clarity.

# Why
- Current `pkg/testutil/test` package is overcrowded and lacks clear separation of concerns
- Mixing expectations, requirements, and core test functionality in one package reduces discoverability
- Module deserves its own dedicated location outside `pkg/`

# Changes

### Module relocation
- `pkg/testutil/test` → `mod/tigron`
- Update all imports across test files
- Module name: `github.com/containerd/nerdctl/mod/tigron`

### Package structure
```
mod/tigron/
├── expect/      # Output comparators (Contains, Equals, Match, ExitCode constants)
├── require/     # Test requirements (Linux, Windows, Binary, Not, All)
├── test/        # Core types (Case, Data, Helpers, Command)
└── utils/       # Utilities (RandomString, etc.)
```

### API changes
- `test.Require(...)` → `require.All(...)`
- `test.Contains(...)` → `expect.Contains(...)`
- `test.Equals(...)` → `expect.Equals(...)`
- `test.Windows` → `require.Windows`
- `test.Binary(...)` → `require.Binary(...)`
- `test.Not(...)` → `require.Not(...)`
- ... (all comparators/requirements similarly namespaced)

### Naming rationale
*"tigron"* = French for "tigon" (tiger × lion offspring) 🐯🦁

# Files affected
- ~70 test files updated with new import paths
- All test files under `cmd/nerdctl/*/` 
- Test infrastructure in `pkg/testutil/nerdtest/`
- Documentation in `docs/testing/tools.md`

# Notes
- Zero functional changes - pure reorganization
- All tests remain compatible
- No impact on production code (test-only changes)