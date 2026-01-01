# Migrate `bevy_sprite` to Required Components

## Summary
Migrate `bevy_sprite` to use required components pattern by making `Sprite` automatically insert `Transform`, `Visibility`, and `SyncToRenderWorld`, and moving image/atlas handles into the `Sprite` component itself.

## Changes

**Component Structure**
- Make `Sprite` require `Transform`, `Visibility`, `SyncToRenderWorld`
- Move `Handle<Image>` into `Sprite::image` field
- Move `TextureAtlas` into `Sprite::texture_atlas` field

**API Changes**
- Deprecate `SpriteBundle` with migration guidance
- Add convenience constructors:
  - `Sprite::from_image(handle)`
  - `Sprite::from_atlas_image(handle, atlas)`
  - `Sprite::from_color(color, size)`
  - `Sprite::sized(size)` (for solid colors)
- Implement `From<Handle<Image>>` for `Sprite`

**Internal Updates**
- Remove all engine uses of `SpriteBundle`
- Update queries to access image/atlas through `Sprite` instead of separate components
- Simplify picking backend (no longer needs `Handle<Image>`, `TextureAtlas` in query)
- Update AABB calculation system
- Update sprite extraction system
- Update texture slicing systems

**Examples**
- Replace `SpriteBundle` → `Sprite` across all examples
- Replace separate `Handle<Image>` component → `Sprite::image` field
- Replace separate `TextureAtlas` component → `Sprite::texture_atlas` field

## Migration Guide

```rust
// Before
commands.spawn(SpriteBundle {
    texture: asset_server.load("icon.png"),
    ..default()
});

// After
commands.spawn(Sprite::from_image(asset_server.load("icon.png")));

// Before (with custom size/color)
commands.spawn(SpriteBundle {
    sprite: Sprite {
        color: Color::srgb(1.0, 0.0, 0.0),
        custom_size: Some(Vec2::new(100.0, 100.0)),
        ..default()
    },
    texture: handle,
    ..default()
});

// After
commands.spawn(Sprite {
    image: handle,
    color: Color::srgb(1.0, 0.0, 0.0),
    custom_size: Some(Vec2::new(100.0, 100.0)),
    ..default()
});

// Or for solid colors
commands.spawn(Sprite::from_color(Color::srgb(1.0, 0.0, 0.0), Vec2::new(100.0, 100.0)));

// Before (texture atlas)
commands.spawn((
    SpriteBundle { texture, ..default() },
    TextureAtlas { layout, index },
));

// After
commands.spawn(Sprite::from_atlas_image(texture, TextureAtlas { layout, index }));
```

⚠️ **Breaking**: Using `Handle<Image>` and `TextureAtlas` as separate components on sprite entities no longer works. Use `Sprite::image` and `Sprite::texture_atlas` fields instead.

## Testing
- ✅ Cargo tests on `bevy_sprite`
- ✅ Multiple sprite examples verified