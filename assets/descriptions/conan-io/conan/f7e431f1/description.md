# Refactor package structure: Move conans.client → conan.internal

## Summary
Refactor codebase to migrate modules from `conans.client.*` namespace to `conan.internal.*`, consolidating internal APIs under a unified structure.

## Why
- Modernize package organization by moving legacy `conans.client` code to `conan.internal`
- Clarify internal vs public API boundaries
- Improve maintainability and code discoverability

## Scope

**REST layer** (`conans.client.rest.*` → `conan.internal.rest.*`):
- auth_manager, conan_requester, remote_credentials, remote_manager
- rest_client, rest_client_v2, client_routes, rest_routes
- file_downloader, file_uploader, download_cache, caching_file_downloader
- pkg_sign, rest_client_local_recipe_index

**Graph layer** (`conans.client.graph.*` → `conan.internal.graph.*`):
- graph, graph_builder, graph_binaries, graph_error
- install_graph, installer, profile_node_definer
- build_mode, compatibility, compute_pid, provides, proxy, python_requires, range_resolver

**Downloaders** (`conans.client.downloaders.*` → `conan.internal.rest.*`):
- Merge into REST module

**Core modules**:
- `conans.client.loader` → `conan.internal.loader` (merge loader_txt)
- `conans.client.migrations` → `conan.internal.api.migrations`
- `conans.client.hook_manager` → `conan.internal.hook_manager`
- `conans.client.source` → `conan.internal.source`
- `conans.client.subsystems` → `conan.internal.subsystems`

**Update all imports** across:
- API layer, subapis, tools, tests, utilities