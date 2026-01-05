# Title
-----
Merge `Style` into `Node` and introduce `ComputedNode` for computed properties

# Summary
-------
Consolidate UI node properties by merging all `Style` fields into `Node` component. Move computed layout properties from `Node` into new `ComputedNode` component. Remove `Style` component entirely.

# Why
---
- **Ergonomics**: Eliminate redundancy of specifying both `Node::default()` and `Style { ... }` for every UI entity
- **Clarity**: Remove confusion about `Style` being a "style system" when it only contained core node properties
- **Architecture**: Separate input properties (`Node`) from computed output (`ComputedNode`)

# Changes
---------
**Core API:**
- All `Style` fields → `Node` fields
- Computed properties (size, layout, etc.) → `ComputedNode`
- `Style` component removed

**Component Structure:**
```rust
// Before
Node { calculated_size, unrounded_size, ... }
Style { width, height, display, ... }

// After  
Node { width, height, display, ... }
ComputedNode { calculated_size, unrounded_size, ... }
```

**Affected Systems:**
- `ui_layout_system`: queries `Node` instead of `Style`, uses `ComputedNode` for outputs
- Layout conversion: `from_style()` → `from_node()`
- All rendering/extraction systems
- Focus, accessibility, clipping, overflow systems
- UI bundles: `NodeBundle`, `ImageBundle`, `ButtonBundle`, `MaterialNodeBundle`

**Codebase Impact:**
- `bevy_ui` crate fully refactored
- All examples updated
- Helper utilities adjusted

# Migration
-----------
**Simple case:**
```rust
// Before
commands.spawn((Node::default(), Style { width: Val::Px(100.), .. }));

// After
commands.spawn(Node { width: Val::Px(100.), .. });
```

**Computed properties:**
```rust
// Before
fn system(nodes: Query<&Node>) {
    let size = nodes.single().size();
}

// After
fn system(computed: Query<&ComputedNode>) {
    let size = computed.single().size();
}
```

# Implementation Notes
---------------------
- `Node` now has `#[require(ComputedNode, ...)]`
- UI queries accessing computed data must use `ComputedNode`
- All `style.field` → `node.field`
- Type aliases like `WithNode` updated to `With<Node>`