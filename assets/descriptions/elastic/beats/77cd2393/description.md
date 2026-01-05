# Title
Replace global logger instances with local logger parameter passing (Part 10)

# Summary
Continue refactoring code to eliminate direct global logger creation (`logp.NewLogger()`) by accepting logger instances as parameters and using named child loggers instead.

# Why
- Remove global logger dependencies for better testability
- Enable proper logger lifecycle management and configuration propagation
- Improve code modularity by explicit dependency injection

# Changes

## Pattern Applied
Replace:
```go
func New(...) {
    log := logp.NewLogger("component")
}
```

With:
```go
func New(..., logger *logp.Logger) {
    log := logger.Named("component")
}
```

## Areas Updated

### Filebeat
- `diagnostics.go`: `gzipRegistry()` now accepts logger parameter
- Input readers: `filestream`, `journald`, `kafka`, `log/harvester`
- Parser components: multiline, JSON, syslog, filter readers
- Registry migration logic

### Libbeat
- Processors: `add_process_metadata`, `add_cloud_metadata`, `decode_xml`, `fingerprint`, `ratelimit`, `registered_domain`, `timestamp`, `translate_*`
- Reader implementations: multiline pattern/while readers, JSON parser, syslog parser
- Elasticsearch output client

### X-Pack Metricbeat
- Azure modules: `app_insights`, `billing`, `monitor`, storage clients
- GCP metadata services: compute, cloudsql, dataproc, redis
- Meraki HTTP paginator
- IIS, Jolokia, Statsd modules

### X-Pack Filebeat
- AWS S3 input script sessions
- Nomad metadata matchers
- CEF/VPC Flow Log processors

# Notes
- All changes maintain backward compatibility through function signature updates
- Test utilities updated to use `logp.NewNopLogger()` or `logptest.NewTestingLogger()`
- Removed some unnecessary global logger info messages (e.g., input registration logs)