# Standardize nullness annotations by migrating to JSpecify

## Summary
Migrate all nullness annotations from multiple annotation libraries (`checker-qual`, `javax.annotation`, `jetbrains.annotations`) to the standardized `org.jspecify.annotations` library.

## Why
- Multiple JDK, tool and library vendors have standardized on [JSpecify nullness annotations](https://jspecify.dev/docs/using/)
- Recent Guava versions no longer provide transitive dependency on `checker-qual` library
- Having multiple annotation libraries for the same purpose creates inconsistency and maintenance burden

## Annotations to Migrate

**@NonNull variants:**
- `org.checkerframework.checker.nullness.qual.NonNull` → `org.jspecify.annotations.NonNull`
- `javax.annotation.Nonnull` → `org.jspecify.annotations.NonNull`
- `org.jetbrains.annotations.NotNull` → `org.jspecify.annotations.NonNull`

**@Nullable variants:**
- `org.checkerframework.checker.nullness.qual.Nullable` → `org.jspecify.annotations.Nullable`
- `javax.annotation.Nullable` → `org.jspecify.annotations.Nullable`
- `org.jetbrains.annotations.Nullable` → `org.jspecify.annotations.Nullable`

## Changes
- Add `org.jspecify:jspecify:1.0.0` dependency to relevant modules
- Replace import statements across codebase (managed-ledger, pulsar-broker, pulsar-client, pulsar-common, pulsar-io/*, pulsar-functions/*, pulsar-proxy)
- Add Checkstyle rules to prevent future introduction of deprecated annotations
- Remove invalid use of `javax.validation.constraints.{Null, NotNull}` (these are for user input validation, not static analysis)
- Update LICENSE files to include JSpecify

## Verification
- All nullness annotations use `org.jspecify.annotations.*`
- Checkstyle enforces no new usage of deprecated annotations
- No compilation or runtime issues