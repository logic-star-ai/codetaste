# Remove global k8s client accessors in favor of explicit Clientset parameter

Eliminate global k8s client accessors (`k8s.Client()`, `k8s.CiliumClient()`, etc.) and refactor all usages to explicitly pass/store `client.Clientset` instead.