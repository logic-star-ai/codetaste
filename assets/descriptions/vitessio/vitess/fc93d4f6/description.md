# Refactor `vtcombo` flags - Part 2

## Summary
Migrate 56 flags in `vtcombo` binary from underscore (`_`) to dash (`-`) naming convention as part of ongoing flag standardization effort.

## Scope
Flags updated in this refactoring:
- `buffer_*` → `buffer-*` (drain-concurrency, keyspace-shards, max-failover-duration, min-time-between-failovers, size, window)
- `gc_*` → `gc-*` (check-interval, purge-check-interval)  
- `health_check_interval` → `health-check-interval`
- `healthcheck_*` → `healthcheck-*` (retry-delay, timeout)
- `heartbeat_on_demand_duration` → `heartbeat-on-demand-duration`
- `hot_row_protection_*` → `hot-row-protection-*` (concurrent-transactions, max-global-queue-size, max-queue-size)
- `transaction_limit_*` → `transaction-limit-*` (by-component, by-principal, by-subcomponent, by-username, per-user)
- `vttablet_skip_buildinfo_tags` → `vttablet-skip-buildinfo-tags`
- `wait_for_backup_interval` → `wait-for-backup-interval`
- `warn_*` → `warn-*` (memory-rows, payload-size, sharded-only)
- `watch_replication_stream` → `watch-replication-stream`
- `xbstream_restore_flags` → `xbstream-restore-flags`

## Changes Required
- Update flag definitions in Go code using `utils.SetFlag*Var()` helpers
- Update flag references in test files
- Update config files (YAML) to reflect new flag names in comments
- Update generated flag documentation/help text
- Maintain backward compatibility via flag aliases (deprecate underscore versions)

## Progress
**Before:** 318 underscore flags, 1760 dash flags  
**After:** 262 underscore flags, 1816 dash flags  
**Migrated:** 56 flags

## Why
Standardize flag naming convention across Vitess binaries for better consistency and user experience.