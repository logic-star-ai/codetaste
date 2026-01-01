# Refactor: Rename "manager" to "pilot" across entire codebase

## Summary
Perform sweeping rename from "manager" to "pilot" throughout the codebase, including package names, binaries, services, documentation, and all references.

## Why
Rebrand the "Istio Manager" component to "Istio Pilot" for better clarity and alignment with Istio terminology.

## Changes Required

### Go Package & Import Paths
- Rename Go module: `istio.io/manager` → `istio.io/pilot`
- Update all import statements across codebase
- Update `go_prefix` in BUILD files

### Binaries & Services
- Rename binary: `cmd/manager` → `cmd/pilot`
- Rename Kubernetes service: `istio-manager` → `istio-pilot`
- Update service discovery address: `istio-manager:8080` → `istio-pilot:8080`
- Update Docker image names: `manager` → `pilot`

### Code Identifiers
- `ManagerClient` → `ConfigClient`
- `managerRegression()` → `regression()`
- `istioManagerAPIService` → `istioConfigAPIService`
- Update CLI flags: `--managerAPIService` → `--configAPIService`
- Update variable/function names containing "manager"

### Documentation & Comments
- Update all occurrences of "Istio Manager" → "Istio Pilot"
- Update all occurrences of "manager" → "pilot" in docs
- Update README.md, CONTRIBUTING.md, design docs
- Fix URLs and badge links (testing.istio.io, goreportcard, godoc, codecov)

### Build & Deployment
- Update Bazel workspace name: `com_github_istio_manager` → `com_github_istio_pilot`
- Rename Docker build files: `manager_docker.bzl` → `debug_docker.bzl`
- Update Jenkinsfile stages and image names
- Update deployment templates (`.yaml.tmpl` files)
- Fix mount paths in Vagrantfile and minikube docs

### Testing
- Update test file paths and golden artifacts
- Update test service names and addresses
- Fix integration test templates and configurations
- Update codecov requirements file

### Scripts
- Update `bin/` scripts (e2e.sh, codecov.sh, cross-compile-istioctl, etc.)
- Fix paths in build and deployment scripts