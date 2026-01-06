# Rename `pkg/controller` to `pkg/reconciler`

Rename `pkg/controller` package to `pkg/reconciler` to better reflect that it contains Reconciler implementations (from `github.com/knative/pkg/controller.Reconciler` interface), not controller implementations.