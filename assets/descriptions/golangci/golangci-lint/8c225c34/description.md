# Title
-----
Simplify linter constructors with single-analyzer helper and fluent config API

# Summary
-------
Introduce `NewLinterFromAnalyzer()` constructor and `WithConfig()` method to reduce boilerplate in 90+ linter definitions that use a single analyzer.

# Why
---
- 90% of linters use only one analyzer → eliminate repetitive `NewLinter(..., []*analysis.Analyzer{a}, ...)` calls
- Config maps always wrap settings under analyzer name as key → automate this pattern
- Current constructors are verbose and repetitive across codebase

# Changes
---------
**New API in `pkg/goanalysis/linter.go`:**
- `NewLinterFromAnalyzer(analyzer *analysis.Analyzer) *Linter` → creates linter from single analyzer
- `WithDesc(desc string) *Linter` → overrides analyzer description
- `WithConfig(cfg map[string]any) *Linter` → auto-wraps config with `lnt.name` as key

**Removed:**
- Unused constants `TheOnlyAnalyzerName` and `TheOnlyanalyzerDoc`

**Updated:**
- Refactor 90+ linter constructors in `pkg/golinters/...` to use new fluent API
- Replace verbose `NewLinter()` + config wrapping with chainable `NewLinterFromAnalyzer().WithConfig().WithLoadMode()`

# Example
---------
**Before:**
```go
a := analyzer.New()
cfg := map[string]map[string]any{
    a.Name: {"key": value},
}
return goanalysis.NewLinter(a.Name, a.Doc, []*analysis.Analyzer{a}, cfg).WithLoadMode(...)
```

**After:**
```go
return goanalysis.
    NewLinterFromAnalyzer(analyzer.New()).
    WithConfig(map[string]any{"key": value}).
    WithLoadMode(...)
```