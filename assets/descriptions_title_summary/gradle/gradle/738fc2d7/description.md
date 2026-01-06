# Restructure :build-cache subproject for reuse outside Gradle

Reorganize build cache modules to enable reuse outside of Gradle by:
- Extracting public API to `:build-cache-spi`
- Moving local cache implementation to `:build-cache-local`
- Breaking dependencies on Gradle-specific types