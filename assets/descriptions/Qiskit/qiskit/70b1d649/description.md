# Title

Refactor: Split quantum-info and synthesis functionality into separate crates

# Summary

Split the monolithic `qiskit-accelerate` crate into two new specialized crates:
- `qiskit-quantum-info`: quantum information data structures and functions
- `qiskit-synthesis`: circuit synthesis algorithms and decompositions

This completes the decomposition of `qiskit-accelerate` into separate compilation units based on functionality, moving it to the end of the dependency tree.

# Why

- **Better dependency management**: Avoid pulling heavy dependencies (`faer`, `faer-ext`) into `qiskit-cext` which only needs quantum-info and circuit functionality
- **Improved build times**: Separate compilation units allow parallel builds and smaller rebuild scopes
- **Clearer separation of concerns**: Synthesis (mathematical operations → circuits) vs quantum-info (modeling quantum information) have distinct purposes
- **Cleaner architecture**: `qiskit-accelerate` becomes a leaf crate, only used by Python interface crates

# New Dependency Tree

```
qiskit-pyext
├── qiskit-accelerate
    ├── qiskit-transpiler
├── qiskit-cext
    ├── qiskit-quantum-info
    ├── qiskit-circuit
├── qiskit-transpiler
    ├── qiskit-synthesis
    ├── qiskit-quantum-info
    ├── qiskit-circuit
├── qiskit-synthesis
    ├── qiskit-quantum-info
    ├── qiskit-circuit
├── qiskit-quantum-info
    ├── qiskit-circuit
├── qiskit-circuit
```

# What Moved

**→ `qiskit-quantum-info`:**
- `sparse_observable/*`
- `sparse_pauli_op`
- `unitary_compose`
- `versor_u2`
- `convert_2q_block_matrix`
- `rayon_ext`

**→ `qiskit-synthesis`:**
- `euler_one_qubit_decomposer`
- `two_qubit_decompose`
- `cos_sin_decomp` (→ `linalg/`)
- `synthesis/*` (clifford, linear, linear_phase, evolution, ...)

**Remains in `qiskit-accelerate`:**
- `circuit_duration` (moved from transpiler)
- `circuit_library`
- `isometry`, `optimize_1q_gates`, `pauli_exp_val`, `sampled_exp_val`
- `results`, `twirling`, `uc_gate`

# Changes

- Update all imports/module paths throughout codebase
- Move utility functions (`getenv_use_multiple_threads` → `qiskit-circuit`)
- Update `Cargo.toml` dependencies for all affected crates
- Update Python bindings in `qiskit-pyext`
- Update cbindgen config for C FFI
- Lock file updates