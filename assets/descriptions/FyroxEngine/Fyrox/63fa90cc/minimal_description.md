# Refactor resource system - consolidate metadata in ResourceHeader

Refactor internal structure of resources to centralize all metadata (path, type UUID, state) in a single `ResourceHeader` struct instead of scattering across `ResourceState` variants and resource data implementations.