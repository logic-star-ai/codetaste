# Consolidate CPU architecture information into `cmd/internal/sys` package

Introduce new `cmd/internal/sys` package to centralize architecture metadata (name, family, byte order, pointer/register sizes) that was previously scattered redundantly across the source tree.

Replace old char-based architecture identifiers ('6', '5', '8', '7', '9', '0', 'z') with named constants (`sys.AMD64`, `sys.ARM`, `sys.I386`, `sys.ARM64`, `sys.PPC64`, `sys.MIPS64`, `sys.S390X`) throughout codebase.