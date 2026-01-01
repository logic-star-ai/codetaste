Title
-----
Extract transpiler functionality into separate `qiskit-transpiler` crate

Summary
-------
Split transpiler code from `qiskit-accelerate` into standalone `qiskit-transpiler` crate to improve organization, dependency management, and prepare for C API exposure.

Why
---
- Transpiler functionality has grown large enough to warrant its own compilation unit
- More explicit interface boundaries needed for C API exposure and internal dependency management
- Part of longer-term vision where pure Rust APIs are separated from Python interface components
- Better organization as transpiler is the next big frontier in the C API

What
----
**New crate structure:**
- Create `crates/transpiler/` with own `Cargo.toml`
- Add `src/passes/mod.rs` organizing all transpiler pass implementations

**Modules moved from `qiskit-accelerate` to `qiskit-transpiler`:**
- `src/passes/`: barrier_before_final_measurement, basis_translator, check_map, commutation_{analysis,cancellation}, consolidate_blocks, dense_layout, elide_permutations, filter_op_nodes, gate_direction, gates_in_basis, high_level_synthesis, inverse_cancellation, optimize_1q_gates_decomposition, remove_diagonal_gates_before_measure, remove_identity_equiv, sabre/*, split_2q_unitaries, star_prerouting, unitary_synthesis, vf2_layout
- `src/target/`: entire target module
- `src/commutation_checker.rs`
- `src/equivalence.rs`
- `src/circuit_duration.rs` (temporary, should move back)
- `src/twirling.rs` (temporary, should move back)

**Updates:**
- Update imports throughout codebase
- Rename pass functions following convention: `{verb}_pass_name` (e.g. `run_check_map`)
- Export submodule builders as `*_mod` functions for qiskit-pyext

Known Limitations
-----------------
- **Not 100% clean separation**: qiskit-transpiler still depends on qiskit-accelerate
  - Synthesis and quantum_info pieces remain in accelerate (need dedicated crate)
  - NLayout module not migrated (blocked on moving PhysicalQubit/VirtualQubit to qiskit-circuit)
- `circuit_duration` and `twirling` temporarily in transpiler due to Target dependency
  - Should move back to accelerate once dependency can be reversed