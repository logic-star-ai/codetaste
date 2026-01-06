# Migrate `bevy_sprite` to Required Components

Migrate `bevy_sprite` to use required components pattern by making `Sprite` automatically insert `Transform`, `Visibility`, and `SyncToRenderWorld`, and moving image/atlas handles into the `Sprite` component itself.