# Rename NFT module to use vanity URL

## Summary

Rename NFT module from `github.com/cosmos/cosmos-sdk/x/nft` to `cosmossdk.io/x/nft` with vanity URL import path.

## Why

Extracted modules must use vanity URLs as decided in #14634. This aligns with the project's architecture for modularization and provides cleaner, more maintainable import paths.

## Changes

**Module Path**
- Changed go module path from `github.com/cosmos/cosmos-sdk/x/nft` → `cosmossdk.io/x/nft`
- Updated `go_package` option in all proto files (event.proto, genesis.proto, nft.proto, query.proto, tx.proto, module.proto)

**Import Updates**
- Updated all imports across simapp, tests, and module code
- Modified go.mod/go.sum files to reference new module path
- Updated replace directives in simapp and tests

**Internal Package**
- Added `x/nft/internal/conv` package for string/bytes conversion utilities
- Moved `UnsafeStrToBytes` and `UnsafeBytesToStr` functions with tests

**Build & Scripts**
- Updated `scripts/protocgen.sh` to handle `cosmossdk.io` path
- Modified go.work.example with new module location

**Documentation**
- Added CHANGELOG entry noting API breaking change

## Impact

**Breaking Change**: All consumers importing `github.com/cosmos/cosmos-sdk/x/nft` must update imports to `cosmossdk.io/x/nft`.