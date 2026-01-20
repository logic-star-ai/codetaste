# Merge `Style` into `Node` and introduce `ComputedNode` for computed properties

Consolidate UI node properties by merging all `Style` fields into `Node` component. Move computed layout properties from `Node` into new `ComputedNode` component. Remove `Style` component entirely.