# Refactor HLE logging functions

## Summary
Consolidate HLE logging into fewer, more logical functions by removing the distinction between format-specific variants (*LogI vs *LogX) and using HLE function metadata to automatically determine return value formatting.

## Changes

### Macro Consolidation
- Replace `hleLogSuccessI/X` → `hleLogDebug`
- Replace `hleLogSuccessInfoI/X` → `hleLogInfo`  
- Replace `hleLogSuccessVerboseI/X` → `hleLogVerbose`
- Replace `hleLogSuccessOrWarn/Error` → `hleLogDebugOrWarn/Error`

### Core Logging Refactor
- Remove `retmask` parameter from `hleDoLog()` - now extracted from HLE function metadata
- Add 'v' (void) return type handling where return values should not be displayed
- Enhance return type formatting logic (x/i/I/f/v cases)
- Mark `hleDoLog()` as `NO_INLINE` for both MSVC and GCC/Clang

### Metadata-Driven Formatting
Return value display format now determined automatically from `hleFunc->retmask`:
- 'x' → hex output (truncated to u32)
- 'i'/'I' → signed/unsigned decimal
- 'f' → float (currently as bits)
- 'v' → void (no return value shown)

## Benefits
- Reduced code duplication across ~200+ call sites
- More consistent logging API
- Simplified function signatures
- Prepares for future error code decoding enhancement

## Future Work
Next step: Add 'e'/'E' return types for automatic error code text decoding (not included to limit scope).