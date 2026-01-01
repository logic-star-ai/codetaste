Title
-----
Replace deprecated `io/ioutil` with `io` and `os` packages

Summary
-------
Replace all usages of the deprecated `io/ioutil` package with their new equivalents in `io` and `os` packages. The `io/ioutil` package has been deprecated since Go 1.16.

Why
---
- `io/ioutil` was deprecated in Go 1.16 (https://golang.org/doc/go1.16#ioutil)
- Vitess now uses Go 1.17+, making this migration appropriate
- Functions have been moved to more appropriate packages (`io` and `os`)
- Maintains compatibility with current Go idioms and best practices

Changes Required
----------------
Replace deprecated functions across the codebase:

- `ioutil.ReadFile` → `os.ReadFile`
- `ioutil.WriteFile` → `os.WriteFile`  
- `ioutil.ReadAll` → `io.ReadAll`
- `ioutil.TempDir` → `os.MkdirTemp`
- `ioutil.TempFile` → `os.CreateTemp`
- `ioutil.NopCloser` → `io.NopCloser`
- `ioutil.ReadDir` → `os.ReadDir` (returns `[]DirEntry` instead of `[]FileInfo`)

Update imports:
- Remove `io/ioutil` imports
- Add `io` and/or `os` imports as needed

Scope
-----
This affects files across:
- `examples/...`
- `go/cmd/...`
- `go/vt/...`
- `go/test/...`
- `go/tools/...`
- `vitess-mixin/...`
- Root level test files