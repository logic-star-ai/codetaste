# Refactor: Migrate copy/stage tests to sqllogic and reorganize test data

## Summary
Migrate shell-based tests for `COPY`, stage operations, and file format handling to sqllogic format. Reorganize test data files into structured directories and update all test references.

## Changes

### Test Migration to Sqllogic
- **NDJSON**: Migrated `select from ndjson` tests → `sqllogictests/suites/stage/formats/ndjson/ndjson_select`
- **Parquet**: 
  - Migrated `ontime_200.parquet` selection tests → `sqllogictests/suites/stage_parquet/on_time`
  - Migrated `select parquet as view` tests → `sqllogictests/suites/stage_parquet/select_parquet`
- **HTTP Copy**: Migrated `copy from http` tests → `sqllogictests/suites/stage/copy_from_http`
- **XML**: Consolidated 6 separate XML test scripts into single unified test → `01_streaming_load/01_0006_streaming_load_xml`

### Test Organization
- Renamed `00_copy/` → `00_stage/` (stage-related operations)
- Renamed `01_load/` → `01_streaming_load/` (streaming load operations)
- Moved distributed copy tests from `00_copy/` → `00_stage/`

### Data File Reorganization
```
tests/data/
├── csv/         (*.csv files)
├── ndjson/      (*.ndjson files)
├── parquet/     (*.parquet files)
└── tsv/         (*.tsv files)
```

- Moved all CSV files into `data/csv/`
- Moved NDJSON files into `data/ndjson/`
- Moved parquet files into `data/parquet/`
- Moved TSV files into `data/tsv/`
- Removed unused files: `nyctaxi.csv`, duplicate `sample_2_columns.csv`

### Infrastructure
- Added `TESTS_DATA_DIR` environment variable to `shell_env.sh` → centralized data path reference
- Updated all remaining shell tests to use `$TESTS_DATA_DIR` instead of hardcoded paths

## Why
- Sqllogic tests are more maintainable and consistent than shell scripts
- Structured data directories improve discoverability and reduce clutter
- Centralized path configuration (`TESTS_DATA_DIR`) reduces test fragility
- Consolidation reduces test duplication and maintenance burden