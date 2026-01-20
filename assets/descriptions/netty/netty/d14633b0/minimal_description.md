# Remove all Java 6/7 version checks and guards after Java 8 baseline bump

Clean up codebase by removing all Java 6/7 compatibility code now that Java 8 is the minimum supported version for Netty 4.2. This includes:
- Removing runtime version checks (`PlatformDependent.javaVersion() >= 7/8`)
- Removing `@SuppressJava6Requirement` annotations
- Removing Java 6/7 fallback implementations
- Using Java 8+ APIs directly without guards