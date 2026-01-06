# Refactor SMP pause mechanism: rename xxxx_pause.c → xxxx_smpcall.c

Rename `*_cpupause.c` files to `*_smpcall.c` across all architectures and update associated function/IRQ handler names to reflect actual SMP semantics.