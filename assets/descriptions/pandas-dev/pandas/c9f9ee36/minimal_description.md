# CLN: De-privatize core.common functions, remove unused utilities

Clean up `pandas.core.common` module by:
- Removing underscore prefix from internal functions (de-privatizing)
- Moving console detection functions to `io.formats.console`
- Removing functions only used in tests or not used at all