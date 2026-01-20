# Consolidate misc/cgo/test files to reduce compilation overhead

Merge multiple small cgo test files into fewer consolidated files to reduce build time. Each file with `import "C"` requires separate cgo compilation/analysis, causing significant overhead.