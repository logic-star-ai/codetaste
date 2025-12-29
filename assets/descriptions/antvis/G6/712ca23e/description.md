# Refactor: Standardize Node Drawing API and Element Conventions

## Summary

Refactor node drawing implementation to follow element conventions, standardize property naming, and improve rendering control.

## Changes

### Naming Conventions
- Rename `anchorOptions` → `ports` (resolve naming conflict with G's anchor/origin)
- Rename `badgeOptions` → `badges`
- Rename `sourceAnchor`/`targetAnchor` → `sourcePort`/`targetPort`
- Rename `getAnchors()` → `getPorts()`, `findAnchor()` → `findPort()`
- Rename `getAnchorPosition()` → `getPortPosition()` and related helpers

### Node Positioning
- Replace `cx, cy, r` with `x, y, width, height` for consistent coordinate system
- Update Circle/Ellipse to internally convert to `cx, cy, rx, ry` for G rendering
- Standardize all node types to use same positioning properties

### Architecture
- Add `Polygon` abstract base class for Triangle, Rect, Star, Diamond, Hexagon, etc.
- Refactor Badges/Ports to use `this.upsert()` for automatic lifecycle management
- Add Z-index control via config properties:
  ```ts
  {
    haloZIndex: -1,
    labelZIndex: 0, 
    iconZIndex: 1,
    portZIndex: 2,
    badgeZIndex: 3
  }
  ```

### Style Properties
- Adjust element attributes following element conventions
- Provide proper parsing/adaptation for attribute handling
- Improve `getKeyStyle()`, `getHaloStyle()`, `getPortStyle()`, `getBadgeStyle()` implementations

### Breaking Changes
- All node position properties changed from `cx/cy/r` to `x/y/width/height`
- `anchorOptions` → `ports`, `badgeOptions` → `badges`
- `sourceAnchor`/`targetAnchor` → `sourcePort`/`targetPort`
- Animation fields updated to reflect new property names

## Why

- Resolve naming confusion between G6's connection points (now "ports") and G's anchor (origin position)
- Establish consistent API across all node types
- Better align with element design conventions
- Improve rendering control and predictability
- Provide cleaner abstraction for polygon-based nodes