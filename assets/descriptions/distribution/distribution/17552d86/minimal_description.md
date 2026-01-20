# Deprecate internal reference package, migrate to extracted module

Migrate from internal `reference` package to external `github.com/distribution/reference` module. The reference functionality has been extracted into a standalone module and the internal package is now deprecated with forwarding wrappers.