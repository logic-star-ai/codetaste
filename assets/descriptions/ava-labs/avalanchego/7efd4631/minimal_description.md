# Refactor mock generation to use local `//go:generate` directives

Improve mock generation workflow by replacing centralized shell scripts with local `//go:generate` directives in `mocks_generate_test.go` files per package. Use `go run go.uber.org/mock/mockgen` for platform-independent, IDE-friendly mock generation.