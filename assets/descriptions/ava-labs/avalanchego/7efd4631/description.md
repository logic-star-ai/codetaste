# Title
-----
Refactor mock generation to use local `//go:generate` directives

# Summary
-------
Improve mock generation workflow by replacing centralized shell scripts with local `//go:generate` directives in `mocks_generate_test.go` files per package. Use `go run go.uber.org/mock/mockgen` for platform-independent, IDE-friendly mock generation.

# Why
---
- Centralized scripts (`scripts/mock.gen.sh`, `scripts/mocks.mockgen.txt`) are hard to maintain and not IDE-friendly
- Requires pre-installing mockgen globally
- Shell scripts not platform-independent
- Difficult to discover which mocks are generated for a given package

# Changes
--------
- **Local mock generation**: Add `mocks_generate_test.go` file per package with `//go:generate go run go.uber.org/mock/mockgen@v0.5` directives
- **Remove scripts**: Delete `scripts/mock.gen.sh`, `scripts/mocks.mockgen.txt`, `scripts/mocks.mockgen.source.txt`
- **Simplify CI**: Update `.github/workflows/ci.yml` to use `grep | xargs | go generate` instead of shell scripts
- **Upgrade mockgen**: v0.4 → v0.5 (adds generic support)
- **Switch to reflect mode**: Replace source mode generation with reflect mode (6 commands)
- **Standardize paths**: Mock destinations now relative to package directory
- **Remove unused mocks**: Delete `api/server/servermock/server.go`
- **Update docs**: Revise `CONTRIBUTING.md` and `README.md` with new workflow

# Benefits
---------
- Generate mocks from IDE directly
- No global mockgen installation required
- Platform-independent (uses `go` only)
- Self-documenting (generation commands colocated with code)
- Simpler CI verification

# Command
-------
```sh
go generate -run "go.uber.org/mock/mockgen" ./...
```