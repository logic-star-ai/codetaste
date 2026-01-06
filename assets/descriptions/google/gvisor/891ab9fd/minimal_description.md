# Move `//pkg/sentry/kernel/time` to `//pkg/sentry/ktime`

Relocate time package from `pkg/sentry/kernel/time/` to `pkg/sentry/ktime/` to eliminate import aliasing requirement.