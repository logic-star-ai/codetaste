# Refactor unwind in MIR

Replace `Option<BasicBlock>` representation of unwinding with explicit `UnwindAction` enum to improve type safety and semantic clarity.