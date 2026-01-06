# Decouple core and plotting APIs to improve imports and tighten public namespace

Refactor PyVista's internal structure to separate `pyvista.core` (data structures, filters) from `pyvista.plotting` (visualization, rendering) to improve modularity, eliminate circular imports, and enable graphics-independent usage of core API.