# Consolidate DAG scheduling parameters into single `schedule` argument

## Summary
Consolidate `schedule_interval`, `timetable`, and `schedule_on` parameters into a unified `schedule` parameter that accepts cron expressions, timedelta objects, Timetable instances, or Dataset lists.

## Why
- Simplifies DAG API by reducing multiple overlapping scheduling parameters to one
- Eliminates confusion about which parameter to use for different scheduling scenarios
- Makes scheduling more intuitive: `schedule=...` for all cases

## Changes

### Core
- Add new `schedule` parameter to `DAG` class accepting: cron string | timedelta | Timetable | List[Dataset]
- Deprecate `schedule_interval` and `timetable` with warnings
- Rename internal `schedule_on` → `dataset_triggers`
- Update validation to accept at most one scheduling argument
- Handle different `schedule` types appropriately (Dataset list → `dataset_triggers`, Timetable → `timetable`, else → `schedule_interval`)

### DAG Examples & Tests
- Replace `schedule_interval=...` → `schedule=...` across all example DAGs
- Replace `schedule_on=[dataset]` → `schedule=[dataset]` for dataset-triggered DAGs
- Update all tests to use new parameter

### Documentation
- Update all docs/tutorials showing `schedule_interval` → `schedule`
- Update timetable docs to reflect new parameter
- Update docstrings and template references

### Serialization
- Update schema: `schedule_on` → `dataset_triggers`
- Update serialization logic for datasets

### Backwards Compatibility
- Existing `schedule_interval` and `timetable` arguments still work with deprecation warnings
- Schedule validation ensures only one of the three arguments is provided