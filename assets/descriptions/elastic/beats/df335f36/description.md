# Title

Replace global logger with local logger instances

# Summary

Refactor codebase to eliminate global logger usage by passing logger instances through function parameters instead of creating/accessing loggers globally.

# Why

- Improves logging architecture and testability
- Enables proper logger scoping and hierarchies
- Better control over logging context
- Aligns with best practices for dependency injection

# Changes

**Function Signatures Updated:**
- Add `logger *logp.Logger` parameter to functions previously using `logp.NewLogger()` or global `logp.*()` methods
- Functions affected: `FetchConfigs()`, `mergeConfigFiles()`, `withLog()`, `NewStateIdentifier()`, `newINodeMarkerIdentifier()`, `NewStates()`, `Send()`, `Start()`, ...

**Logger Instantiation:**
- Replace standalone `logp.NewLogger()` calls with logger instances passed from parent contexts
- Use `base.Logger().Named()` in metricsets
- Use `beat.Info.Logger` in inputs
- Use `logptest.NewTestingLogger(t, "")` in tests

**Global Logger Methods Replaced:**
- `logp.Info()` → `logger.Infof()`
- `logp.Err()` → `logger.Errorf()`
- `logp.Debug()` → `logger.Named().Debugf()`

**Modules Affected:**
- `filebeat/beater`, `filebeat/config`, `filebeat/fileset/*`
- `filebeat/harvester/*`, `filebeat/input/*` (log, file, filestream, redis, stdin, syslog, mqtt, netmetrics, journald)
- `filebeat/registrar/*`
- `x-pack/auditbeat/module/system/*`
- `x-pack/filebeat/input/*` (awss3, httpjson, netflow)
- `x-pack/metricbeat/module/*` (aws, azure, gcp, iis, meraki, mssql, openai, panw, stan, cloudfoundry, awsfargate)

# Notes

Part of larger initiative to modernize logging practices across Beats codebase (iteration #7).