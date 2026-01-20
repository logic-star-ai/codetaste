# Change TaskInstance and TaskReschedule PK from execution_date to run_id

Replace `execution_date`-based primary key with `run_id`-based primary key for `TaskInstance` and `TaskReschedule` tables. Add explicit foreign key constraint from `TaskInstance` to `DagRun`.