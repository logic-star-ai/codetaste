# Title
-----
Integrate Rect and Vec types throughout library

# Summary
-------
Refactor the library to deeply integrate `Rect`, `Vec2`, and `Vec3` types across sprites, cameras, textures, GUI, and type system. Make these types more accessible and Pythonic while improving API consistency.

# Changes
---

### Core Type System
- Add `Rect`, `Vec2`, `Vec3`, `Vec4` to top-level `arcade` module for easier access
- Add type aliases `Point2` and `Point3` for better type annotations
- Remove obsolete aliases: `IntRect`, `FloatRect`, `RectList`
- Rename `arcade.gui.Rect` → `GUIRect` to avoid naming conflicts
- Functions expecting `Vec2` now accept `Tuple[AsFloat, AsFloat]`

### Rect Enhancements
- `__contains__` - support `point in rect` checks
- `__mul__` / `__truediv__` - scale Rect relative to `(0, 0)`
- `__bool__` - returns `True` if area ≠ 0
- `__round__`, `__floor__`, `__ceil__` - coordinate rounding
- `.area` property
- `.distance_from_bounds(point)` - distance from rect boundary
- `.position_to_uv(point)` - convert pixel position to UV space
- `.uv_to_position(uv)` - convert UV coords to pixels
- Improved docstrings and `.viewport` fix

### Sprite Integration
- `BasicSprite.rect` - returns bounding `Rect`
- `BasicSprite.scale_xy` now returns `Vec2` (was tuple)
- `SpriteSolidColor.from_rect(rect, ...)` constructor
- `NinePatchTexture.from_rect(rect, ...)` constructor

### Camera Vectorization
- All camera functions accept `Point`, `Point2`, or `Point3` where points are expected
- All camera functions return `Vec2`/`Vec3` instead of tuples
- `Camera2D.position` now returns `Vec2`
- Viewport handling uses `Rect` instead of tuples
- Projectors accept viewport/scissor as `Rect`
- Remove viewport from `ProjectionData` protocol

### Additional Integrations
- `Texture.draw_rect(rect, alpha)` - draw texture to rect
- `Section.rect` - get section bounds as Rect
- `Window.rect` - get window bounds as Rect

### Documentation
- Extensive docstring improvements for `Rect`, camera types, and vector types
- Better type hints throughout
- Comments explaining intentional design decisions

# Why
---
- Improve API consistency and discoverability
- Make library more Pythonic with dunder methods
- Better type safety and IDE support
- Easier for beginners with top-level imports
- Reduce tuple unpacking boilerplate
- Better integration between different library subsystems