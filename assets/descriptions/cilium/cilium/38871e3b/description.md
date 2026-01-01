# Title
Migrate pkg/clustermesh to slog

# Summary
Replace logrus with slog for structured logging in the `pkg/clustermesh` package and related components.

# Why
- Modernize logging infrastructure by adopting Go's standard `log/slog` package
- Standardize logging patterns across the codebase
- Improve logging consistency and performance

# Changes

**Core Package Migration:**
- Replace `logrus.FieldLogger` → `*slog.Logger` across all clustermesh components
- Update logging calls to use slog's key-value structured format
- Remove package-level logrus logger instances

**Pattern Changes:**
- `log.WithField(k, v).Info(msg)` → `log.Info(msg, k, v)`
- `log.WithError(err).Error(msg)` → `log.Error(msg, logfields.Error, err)`
- `log.WithFields(logrus.Fields{...})` → `log.With(...)` or inline key-value pairs

**Affected Components:**
- `pkg/clustermesh/*` - core clustermesh functionality
- `clustermesh-apiserver/*` - API server and subpackages (health, metrics, etcdinit, kvstoremesh, mcsapi)
- `pkg/clustermesh/endpointslicesync/*` - endpoint slice synchronization
- `pkg/clustermesh/operator/*` - operator components
- `pkg/dial/dialer.go` - custom dialer with slog
- `pkg/kvstore/etcdinit/init.go` - etcd initialization

**Additional Updates:**
- Add new etcd-related logfields (EtcdDataDir, EtcdClusterName, EtcdUsername, etc.)
- Update test helpers to use `hivetest.Logger(t)` instead of `logrus.New()`
- Update daemon/operator initialization to pass slog loggers
- Add `LogRegisteredSlogOptions()` helper function