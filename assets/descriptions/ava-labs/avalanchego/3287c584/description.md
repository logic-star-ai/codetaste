# Refactor: Remove redundant "Test" prefix/suffix from `*test` package identifiers

## Summary

Remove `Test*`/`*Test` naming from test doubles and helpers in `*test` packages. Package-qualified names like `enginetest.TestEngine` become `enginetest.Engine`, eliminating stuttering per Go style guidelines.

## Why

Test package names (`enginetest`, `blocktest`, `vertextest`, etc.) already indicate testing context. Additional "Test" prefix/suffix creates redundant package-qualified names. Per Google Go style guide on repetition, avoid stuttering when types are always referenced with package qualifier.

## Changes

### Naming
- **Test doubles**: `Test*` → base name
  - `enginetest.TestEngine` → `enginetest.Engine`
  - `blocktest.TestVM` → `blocktest.VM`
  - `vertextest.TestBuilder` → `vertextest.Builder`
  - `validatorstest.TestState` → `validatorstest.State`
- **Stubs**: `FakeSender` → `SenderStub`
- **Constants**: `TestIntSize` → `IntSize`
- **Collections**: `CacherTests` → `Tests`

### Structure
- Test suites use `NamedTest`/`AliasTest` wrappers with `Name` + `Test` fields
- Added `RunAll()` helper functions
- Tests run as subtests via `t.Run()` where applicable
- Function signatures standardized to `(testing.TB, ...params)` order

### Affected Packages
```
cache/cachetest
codec/codectest
ids/idstest, ids/galiasreader  
network/p2p/...
snow/engine/avalanche/vertex/vertextest
snow/engine/enginetest
snow/engine/snowman/block/blocktest
snow/networking/sender/sendertest
snow/validators/validatorstest
vms/.../test helpers
wallet/.../utxotest
```

### Example
```go
// Before
sender := &enginetest.SenderTest{T: t}
for _, test := range codectest.Tests {
    test(codec, t)
}

// After
sender := &enginetest.Sender{T: t}
codectest.RunAll(t, func() codec.GeneralCodec { 
    return NewCodec() 
})
```

## Compatibility
`validatorstest.TestState` aliased to `State` for coreth compatibility