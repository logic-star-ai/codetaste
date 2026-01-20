# Unify scheduler context switch calls with `nxsched_switch_context` across architectures

Replace all separate `nxsched_suspend_scheduler`/`nxsched_resume_scheduler` calls with unified `nxsched_switch_context(prev, next)` across all architecture implementations.