# Refactor: Split quantum-info and synthesis functionality into separate crates

Split the monolithic `qiskit-accelerate` crate into two new specialized crates:
- `qiskit-quantum-info`: quantum information data structures and functions
- `qiskit-synthesis`: circuit synthesis algorithms and decompositions

This completes the decomposition of `qiskit-accelerate` into separate compilation units based on functionality, moving it to the end of the dependency tree.