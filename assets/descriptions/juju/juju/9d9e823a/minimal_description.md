# Remove juju/errors dependency from core package

Remove `juju/errors` from the core package and replace with internal error handling (`core/errors` and `internal/errors`). Migrate to Go 1.13+ error wrapping patterns.