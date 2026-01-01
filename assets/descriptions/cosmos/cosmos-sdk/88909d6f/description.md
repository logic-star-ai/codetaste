# Refactor: Rename Tendermint to CometBFT

## Summary
Rename all Tendermint references to CometBFT throughout the codebase, including imports, variable names, function names, types, comments, and file names.

## Why
The consensus engine has been renamed from Tendermint to CometBFT. The codebase needs to reflect this change for consistency and clarity.

## Changes

### Import Paths
- Rename all import aliases: `tm*` → `cmt*`
  - `tmproto` → `cmtproto`
  - `tmtypes` → `cmttypes`  
  - `tmcrypto` → `cmtcrypto`
  - `tmbytes` → `cmtbytes`
  - `tmcfg` → `cmtcfg`
  - `tmcli` → `cmtcli`
  - `tmjson` → `cmtjson`
  - ... (etc)

### Files Renamed
- `client/tendermint.go` → `client/cometbft.go`
- `crypto/codec/tm.go` → `crypto/codec/cmt.go`
- `server/tm_cmds.go` → `server/cmt_cmds.go`
- `x/simulation/mock_tendermint.go` → `x/simulation/mock_cometbft.go`
- `x/staking/testutil/tm.go` → `x/staking/testutil/cmt.go`

### Types & Functions
- `TendermintRPC` → `CometRPC`
- `MockTendermintRPC` → `MockCometRPC`
- `ToTmValidator()` → `ToCmtValidator()`
- `GetTmConsPubKey()` → `GetCmtConsPubKey()`
- `FromTmProtoPublicKey()` → `FromCmtProtoPublicKey()`
- `ToTmProtoPublicKey()` → `ToCmtProtoPublicKey()`
- ... (all `Tm*` / `tm*` prefixed items)

### Comments & Documentation
- Update all comments referencing "Tendermint" to "CometBFT"
- Update `UPGRADING.md` with migration notes
- Update server command descriptions
- Update config templates (TOML)

### Module Dependencies
- Update go.mod/go.sum files across all modules
- Update replace directives for CometBFT compatibility
- Bump protobuf versions as needed

### Test Utilities
- Rename test helper functions in `testutil/` packages
- Update mock implementations
- Update CLI test utilities

## Scope
This refactoring is **limited to naming only** - no functional changes, API endpoints, or breaking changes to external interfaces. A separate PR will handle API/endpoint aliasing.

## Files Modified
- `baseapp/*` - Context creation, ABCI handlers
- `client/*` - RPC interfaces, CLI utilities  
- `crypto/*` - Key codec utilities
- `server/*` - Server commands, config
- `simapp/*` - Test application
- `store/*` - Test utilities
- `x/*` - All module tests, keepers, simulation
- Go module files across workspace