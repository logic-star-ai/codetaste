# Title
-----
Remove global k8s client accessors in favor of explicit Clientset parameter

# Summary
-------
Eliminate global k8s client accessors (`k8s.Client()`, `k8s.CiliumClient()`, etc.) and refactor all usages to explicitly pass/store `client.Clientset` instead.

# Why
---
- Global state makes dependencies implicit and harder to test
- Explicit dependency injection improves code clarity and testability
- Removes hidden coupling through global variables

# Changes
---------

**Remove global accessors:**
- Delete `k8s.Client()`, `k8s.CiliumClient()`, `k8s.APIExtClient()`, `k8s.WatcherClient()`, etc.
- Delete `k8s.SetClients()` function
- Delete `k8s.IsEnabled()` in favor of `clientset.IsEnabled()`
- Remove `pkg/k8s/client.go` and `pkg/k8s/config.go`

**Refactor method signatures:**
- Convert methods like `K8sClient.AnnotateNode()` → `k8s.AnnotateNode(clientset, ...)`
- Convert methods like `K8sClient.GetSecrets()` → removed (use clientset directly)
- Pass `clientset` parameter to all functions/constructors that need k8s access

**Update structs:**
- Add `clientset client.Clientset` field to structs that need k8s access
- Remove wrapper types: `K8sClient`, `K8sCiliumClient`, `K8sSlimClient`, `K8sAPIExtensionsClient`

**Pattern:**
```go
// Before
k8s.CiliumClient().CiliumV2().CiliumNodes().Get(...)

// After  
clientset.CiliumV2().CiliumNodes().Get(...)
```

# Scope
------
Touches ~50+ files across daemon, operator, ipam, watchers, bgp, policy groups, node discovery, device manager, etc.