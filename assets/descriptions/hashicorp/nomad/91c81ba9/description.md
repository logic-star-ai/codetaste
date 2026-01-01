# Title

Rename SecureVariables to Variables throughout codebase

# Summary

Rename "Secure Variables" feature to "Variables" across all Go code following internal terminology decision.

# Why

Internal discussion led to simplifying feature name from "Secure Variables" to "Variables".

# Scope

**API Layer**
- Structs: `SecureVariable*` → `Variable*`
- Endpoints: `/v1/vars`, `/v1/var/*`
- RPC methods: `SecureVariables.*` → `Variables.*`

**ACL System**
- Policies: `secure_variables` → `variables`
- Capabilities: `SecureVariablesCapability*` → `VariablesCapability*`
- Permission checks: `AllowSecureVariableOperation` → `AllowVariableOperation`

**State Store**
- Tables: `TableSecureVariables` → `TableVariables`
- Operations: `SVE*` → `Var*` (e.g., `SVESet` → `VarSet`)
- Quota tracking: `SecureVariablesQuota` → `VariablesQuota`

**CLI Commands**
- `operator secure-variables keyring` → `operator root keyring`
- All subcommands: `install`, `list`, `remove`, `rotate`

**Internal Types**
- `SVOp`/`SVOpResult` → `VarOp`/`VarOpResult`
- `SecureVariableEncrypted` → `VariableEncrypted`
- `SecureVariableDecrypted` → `VariableDecrypted`
- `SecureVariableMetadata` → `VariableMetadata`
- `SecureVariableItems` → `VariableItems`

**Affected Components**
- FSM apply/restore logic
- Snapshot persistence
- Search contexts
- Mock generators
- Test fixtures
- Error messages

# Exclusions

- UI code (separate PR)
- Documentation (separate PR)
- Function-local variables (`sv := ...`)