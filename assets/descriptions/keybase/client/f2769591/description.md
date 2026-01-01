# Refactor message wrapper for improved rendering performance

## Summary
Restructure chat message rendering to improve recycling performance by splitting generic wrapper into type-specific components, reducing prop drilling via Context, and optimizing list rendering.

## Why
Current implementation uses a top-level generic component that splits into children with internal keys, making message recycling slow. This causes performance issues especially on Android 13 and when scrolling through large conversations.

## Changes

### Component Architecture
- Split generic `Message` wrapper into type-specific wrappers (`WrapperText`, `WrapperAttachment`, `WrapperPayment`, etc.)
- Extract shared logic into helper functions and hooks (`useCommon`, `useMessageNode`, etc.)
- Use Context API (`ConvoIDContext`, `OrdinalContext`, `GetIdsContext`) to avoid prop drilling of conversationIDKey/ordinal through hierarchy
- Memoize inner components (message content, left/right sides, reactions, etc.) for better recyclability

### List Rendering
- Create `messageTypeMap` mapping ordinals → types to reduce thrashing
- Remove `measure` callback - components just render, parents handle resizing
- Use built-in `onEndReached` for loading more messages (remove index-watching workaround)
- Reverse indexes in native FlashList (fixes issues with inverted lists)
- Use `ItemSeparatorComponent` for orange line/author logic instead of passing `previous` ordinal to each message
- Desktop: Keep waypoint-based rendering but memoize children more aggressively

### Performance Fixes
- **Android**: Use `undefined` instead of `'transparent'` for backgroundColor to enable collapse optimization while avoiding overdraw
- **Android 13**: Fix major perf issue with scaleY transform - use direct `scaleY: -1` style instead of `transform: [{scaleY: -1}]`
- **iOS**: Fix exploding message animation broken by previous `dynamicColor` changes
- Remove spinner from placeholder messages (shown briefly during high CPU, slows downloads)

### UI/UX
- Desktop `...` menu now appears on hover and overlays content (no permanent space) when no other side items present - pure CSS, no state thrashing
- Cleanup old container/connector patterns throughout

### Misc
- Fix Android emulator compatibility
- Enable/disable "why did you render" tool via config flag
- Remove outdated component logic and unused code paths