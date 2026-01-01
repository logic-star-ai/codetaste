# Change TaskInstance and TaskReschedule PK from execution_date to run_id

## Summary

Replace `execution_date`-based primary key with `run_id`-based primary key for `TaskInstance` and `TaskReschedule` tables. Add explicit foreign key constraint from `TaskInstance` to `DagRun`.

## Why

Part of AIP-39 implementation:
- `execution_date` is not truly unique (multiple runs can share same execution_date)
- `run_id` provides proper uniqueness per DagRun
- Enforces referential integrity at database level
- Eliminates possibility of orphaned TaskInstances

## Database Schema Changes

**TaskInstance PK:**
- Before: `(dag_id, task_id, execution_date)`
- After: `(dag_id, task_id, run_id)`

**TaskReschedule PK:**
- Before: `(dag_id, task_id, execution_date, ...)`  
- After: `(dag_id, task_id, run_id, ...)`

**New FK Constraint:**
```sql
TaskInstance.{dag_id, run_id} → DagRun.{dag_id, run_id} ON DELETE CASCADE
```

## What Was Removed

Scheduler cleanup code for orphaned TaskInstances (no longer possible):
- `_change_state_for_tis_without_dagrun()`
- `_clean_tis_without_dagrun()`
- Config option: `clean_tis_without_dagrun_interval`

## Breaking Changes

- **TaskInstances now require DagRun** (database-enforced)
- `TaskInstance(task, execution_date=...)` deprecated → use `TaskInstance(task, run_id=...)`
- Direct TI manipulation without DagRun will raise FK violation
- Pre-upgrade: manually resolve any dangling TaskInstances

## Migration Notes

- Migration script auto-populates `run_id` from `DagRun.execution_date` join
- Kubernetes: fallback logic for pods with old `execution_date` labels
- Tests updated to always create DagRun with TaskInstance

## API Impact

Updated methods to accept `run_id` instead of `execution_date`:
- TaskInstance constructor
- Executor task keys
- API endpoints
- CLI commands