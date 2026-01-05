# Title
Remove deprecated MobX models and observer wrappers

# Summary
Clean up legacy state management by removing all MobX models, the root store, and observer wrappers. Migrate remaining functionality to React Query / standalone modules.

# Changes

## Deleted Models & Store
- Delete `RootStoreModel` and entire store setup
- Remove `MeModel`, `SessionModel`, `ShellUiModel`
- Delete cache models: `HandleResolutionsCache`, `LinkMetasCache`, `PostsCache`, `ProfilesCache`
- Remove `updateDataOptimistically` helper

## Component Updates
- Strip `observer()` wrappers from all components
- Update components to use session/agent directly instead of `useStores()`
- Remove `RootStoreProvider` from app initialization
- Simplify app startup (no `setupState()` call)

## Refactored Functionality
- Move `ImageSizesCache` → `lib/media/image-sizes.ts` as standalone module
- Update `getLinkMeta()` to accept `BskyAgent` instead of `RootStoreModel`
- Remove deprecated `resolveName()` function
- Move `AppInfo` type to `lib/analytics/analytics.tsx`

## Login & Settings
- Update login screen to use `useServiceQuery()` instead of store
- Update settings to use query client for profile invalidation
- Simplify modal initialization

# Why
Complete the migration to React Query by removing all remaining MobX dependencies and deprecated models that are no longer needed.