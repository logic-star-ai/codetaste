# Refactor geom2 internal representation from sides to outlines

Change geom2 data structure from storing `sides` (edge pairs) to storing `outlines` (ordered point arrays). This eliminates the need for graph traversal when producing outlines, improving performance and reducing memory allocations.