Title
-----
Inline goto targets and reduce variable scope in compiler

Summary
-------
Mechanical refactoring of C->Go conversions using rsc.io/grind tool to improve code structure.

Changes
-------
- Inline goto targets when block is unreachable except through that goto
- Replace `goto ret` with direct `return` statements
- Move variable declarations closer to first use (reducing scope)
- Remove long-distance gotos and unused labels

Affected Areas
--------------
- cmd/5g, cmd/6g, cmd/8g, cmd/9g (architecture-specific code generators)
- cmd/internal/gc (compiler internals)
- cmd/internal/ld (linker)
- cmd/internal/obj (object file handling)
- cmd/internal/asm (assembler)

Technical Details
-----------------
- Gotos previously prevented moving declarations due to scope restrictions
- Inlining criteria: target unreachable except through goto + no variable name conflicts
- Goto to plain return → direct return (even with other paths to same return)

Verification
------------
- Bit-for-bit compatibility checked with toolstash + buildall
- Performance: ~12% reduction in compiler runtime for html/template