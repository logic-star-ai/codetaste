# Refactor Statistics with Precision Estimates (`Exact`, `Inexact`, `Absent`)

Introduce `Precision<T>` enum to track exactness of statistics throughout query planning and execution, replacing the coarse-grained `is_exact` boolean and ambiguous optional fields.