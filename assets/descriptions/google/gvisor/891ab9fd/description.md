# Title

Move `//pkg/sentry/kernel/time` to `//pkg/sentry/ktime`

# Summary

Relocate time package from `pkg/sentry/kernel/time/` to `pkg/sentry/ktime/` to eliminate import aliasing requirement.

# Why

Current location at `//pkg/sentry/kernel/time` forces every import to use aliasing (`ktime "...pkg/sentry/kernel/time"`) to avoid conflicts with Go's stdlib `time` package. Moving to `//pkg/sentry/ktime` aligns package name with common usage pattern.

# Changes

- Move package directory: `pkg/sentry/kernel/time/` → `pkg/sentry/ktime/`
- Rename main file: `time.go` → `ktime.go`
- Update package declaration: `package time` → `package ktime`
- Update ~60+ import statements across codebase
- Remove unnecessary `ktime` import aliases
- Update BUILD dependencies: `//pkg/sentry/kernel/time` → `//pkg/sentry/ktime`
- Fix go_template_instance configs in affected BUILD files

# Scope

Affects imports in:
- contexttest, control, fsimpl/..., fsutil
- kernel/..., msgqueue, semaphore, shm
- socket/..., hostinet, netlink, netstack, unix
- syscalls/linux/...
- vfs, watchdog, seccheck