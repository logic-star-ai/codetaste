# Rename `Logger` to `LegacyLogger` to avoid naming conflict with BrowserKit

Rename the existing `Logger` struct to `LegacyLogger` across the entire codebase to prevent name collision when introducing the new `Logger` from BrowserKit.