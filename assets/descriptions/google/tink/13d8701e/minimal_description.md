# Refactor: Extract registry and keyset packages from tink core

Move `registry` and `keyset` functionality out of the `tink` package into their own dedicated packages. This eliminates protobuf dependencies from both `tink` and `subtle` packages.