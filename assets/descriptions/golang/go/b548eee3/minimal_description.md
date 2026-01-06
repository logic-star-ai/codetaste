# Refactor poller into new internal/poll package

Extract poller functionality from `net` package into new `internal/poll` package to enable reuse by `os` package.