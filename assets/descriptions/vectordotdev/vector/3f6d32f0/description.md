Title
-----
Migrate away from deprecated `chrono` functions to `_opt` variants

Summary
-------
Replace deprecated `chrono` date/time construction functions with their non-panicking `_opt` counterparts throughout the codebase in preparation for upgrading the `chrono` dependency.

Why
---
Deprecated `chrono` functions panic when inputs (month, day, hour, etc.) are out of range. The `_opt` variants return `Option` instead, providing safer error handling. This change is required before upgrading `chrono`.

What Changed
------------
- `NaiveDateTime::from_timestamp(...)` → `...::from_timestamp_opt(...).expect("invalid timestamp")`
- `Utc.ymd(...).and_hms_nano(...)` → `...and_hms_nano_opt(...).expect("invalid timestamp")`
- `Utc.timestamp(...)` → `...timestamp_opt(...).single().expect("invalid timestamp")`
- `NaiveDate::from_ymd(...)` → `...from_ymd_opt(...).expect("invalid date")`
- `NaiveTime::from_hms(...)` → `...from_hms_opt(...).expect("invalid timestamp")`
- `FixedOffset::east(...)` → `...east_opt(...).expect("invalid timestamp")`
- `Utc.timestamp_millis(...)` → `...timestamp_millis_opt(...).single().expect("invalid timestamp")`
- `.and_hms(...)` → `.and_hms_opt(...).expect("invalid timestamp")`

Scope
-----
99% mechanical changes applied across:
- Sinks: `aws_cloudwatch_metrics`, `datadog`, `elasticsearch`, `gcp`, `humio`, `influxdb`, `sematext`, `splunk_hec`
- Sources: `aws_ecs_metrics`, `aws_s3`, `aws_sqs`, `datadog_agent`, `dnstap`, `fluent`, `gcp_pubsub`, `journald`, `splunk_hec`, `syslog`
- Transforms: `log_to_metric`, `metric_to_log`
- Libraries: `codecs`, `enrichment`, `loki-logproto`, `value`, `vector-common`, `vector-core`, `vrl`
- Tests & benchmarks

Behavioral Change
-----------------
No easy way to construct `DateTime` with nanoseconds using new API - affects `lua` transform. Not considered a breaking change.