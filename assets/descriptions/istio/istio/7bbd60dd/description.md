Title
-----
Rename `mixer/pkg/runtime2` to `mixer/pkg/runtime`

Summary
-------
Rename the `mixer/pkg/runtime2` package to `mixer/pkg/runtime` to remove the temporary "2" suffix and establish the canonical package name.

Why
---
The `runtime2` naming was likely used during development/migration. Now that the implementation is stable, we should use the canonical `runtime` name.

Changes
-------
- Move all files from `mixer/pkg/runtime2/*` to `mixer/pkg/runtime/*`
- Update all import statements across the codebase:
  - `istio.io/istio/mixer/pkg/runtime2` → `istio.io/istio/mixer/pkg/runtime`
  - `istio.io/istio/mixer/pkg/runtime2/config` → `istio.io/istio/mixer/pkg/runtime/config`
  - `istio.io/istio/mixer/pkg/runtime2/dispatcher` → `istio.io/istio/mixer/pkg/runtime/dispatcher`
  - `istio.io/istio/mixer/pkg/runtime2/handler` → `istio.io/istio/mixer/pkg/runtime/handler`
  - `istio.io/istio/mixer/pkg/runtime2/routing` → `istio.io/istio/mixer/pkg/runtime/routing`
  - `istio.io/istio/mixer/pkg/runtime2/validator` → `istio.io/istio/mixer/pkg/runtime/validator`
  - `istio.io/istio/mixer/pkg/runtime2/testing/...` → `istio.io/istio/mixer/pkg/runtime/testing/...`
- Update package declarations from `package runtime2` to `package runtime`
- Update variable names (e.g., `mixerRuntime2` → `runtime`)
- Update code comments referencing "runtime2"
- Update codecov configuration files (`codecov.requirement`, `codecov.skip`)

Scope
-----
- `mixer/cmd/mixs/cmd/...`
- `mixer/pkg/api/...`
- `mixer/pkg/server/...`
- All subpackages under the renamed directory