# Refactor: Extract security module from runtime into standalone component

Move the security module from `src/runtime/security/` to `src/security/` to establish it as an independent component with reduced dependencies. Create dedicated test suite `dsn_security_tests` separate from `dsn_runtime_tests`.