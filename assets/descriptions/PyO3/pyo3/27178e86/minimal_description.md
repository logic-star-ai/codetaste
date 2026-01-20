# Remove all functionality deprecated in PyO3 0.23 (except `IntoPy` and `ToPyObject`)

Clean up codebase by removing all deprecated APIs from PyO3 0.23. The `IntoPy` and `ToPyObject` traits are kept for separate handling due to complex fallback logic in macros.