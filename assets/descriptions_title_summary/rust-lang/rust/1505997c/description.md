# Replace `rustc_target` with `rustc_abi` imports across compiler crates

Refactor compiler crates to directly use `rustc_abi` instead of `rustc_target` for ABI-related types. Apply systematic substitutions:
- `rustc_target::spec::abi::Abi` → `rustc_abi::ExternAbi`
- `rustc_target::abi::call` → `rustc_target::callconv`
- `rustc_target::abi` → `rustc_abi`