# Refactor Backend Names

## Summary

Rename backend types and traits to improve clarity and follow Rust naming conventions. This includes changing autodiff-related names from `AD*` to `Autodiff*`, removing the `Backend` suffix from backend types, and introducing type aliases to simplify backend trait implementations.

## Naming Changes

**Autodiff Types:**
- `ADBackendDecorator` → `Autodiff`
- `ADBackend` → `AutodiffBackend` 
- `ADModule` → `AutodiffModule`
- `ADTensor` → `AutodiffTensor`
- `TestADBackend` → `TestAutodiffBackend`
- `TestADTensor` → `TestAutodiffTensor`

**Backend Types (remove suffix):**
- `NdArrayBackend` → `NdArray`
- `TchBackend` → `LibTorch` + `TchDevice` → `LibTorchDevice`
- `WgpuBackend` → `Wgpu`
- `CandleBackend` → `Candle`

## Why

- Follow Rust naming conventions: use `UpperCamelCase` for acronyms/contractions (e.g., `Autodiff` not `AD`)
- Remove redundant `Backend` suffix since types are in `burn::backend` namespace
- Improve clarity: `Autodiff<LibTorch>` is clearer than `ADBackendDecorator<TchBackend>`
- Emphasize behavior (autodiff) over pattern (decorator) in naming
- Better match actual underlying library names (LibTorch vs tch bindings)

## Type Aliases

Introduce type aliases to simplify backend implementations:
- `FloatTensor<B, D>`, `IntTensor<B, D>`, `BoolTensor<B, D>`
- `FloatElem<B>`, `IntElem<B>`
- `Device<B>`
- `FullPrecisionBackend<B>`

## Breaking Changes

- All backend type names changed (breaking for imports/declarations)
- Re-exported aliases like `WgpuAutodiffBackend` removed (users should use `Autodiff<Wgpu>` directly)
- Trait names changed (`ADBackend` → `AutodiffBackend`, etc.)

Users now access actual backend documentation instead of small re-export aliases.