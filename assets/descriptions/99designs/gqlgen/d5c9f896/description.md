# Title

Refactor: use 'any' instead of 'interface{}' for consistency

# Summary

Replace all occurrences of `interface{}` with `any` throughout the codebase (excluding generated files). Enable `revive.use-any` linter rule to enforce this convention going forward.

# Why

- **Modernization**: Leverage Go 1.18+ type alias for cleaner, more readable code
- **Consistency**: Standardize type declarations across the entire codebase
- **Maintainability**: Prevent future uses of `interface{}` through linter enforcement

# Scope

Replace `interface{}` with `any` in:
- `_examples/**` ... all example code, resolvers, tests
- `client/**` ... client types, options, SSE, websocket
- `codegen/**` ... args, data, directives, fields, templates, testservers
- `graphql/**` ... coercion, context, handlers, marshalers, unmarshalers, cache, response
- `graphql/handler/**` ... server, transports, extensions
- `complexity/**` ... complexity calculation
- `plugin/federation/**` ... entity resolvers, runtime

# Exclusions

Maintain `interface{}` for backwards compatibility in:
- `graphql/map.go`
- `codegen/testserver/followschema/resolver.go`
- `codegen/testserver/singlefile/resolver.go`

# Configuration

Add to `.golangci.yml`:
```yaml
rules:
  - name: use-any
```