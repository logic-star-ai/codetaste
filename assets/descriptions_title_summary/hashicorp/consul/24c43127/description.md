# Refactor: Decouple troubleshoot module from consul top-level module

Refactor troubleshoot into an independent Go module to enable import into consul-k8s without pulling in all of consul's dependencies. Create new `envoyextensions` module for shared code between xds and troubleshoot packages.