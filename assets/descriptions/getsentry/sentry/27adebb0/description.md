# Refactor: Move avatar components to `components/core/avatar`

## Summary
Reorganize avatar components under `components/core/avatar` directory and standardize their APIs to consistently use `forwardRef` and export prop types.

## Changes Made

### File Structure
- Moved all avatar components from `components/avatar/*` to `components/core/avatar/*`
- Created deprecation wrappers in old locations for gradual migration
- Left `AvatarList`, `SeenByList`, and `SuggestedAvatarStack` in original location (will be moved separately)

### API Standardization
- All avatar components now use `forwardRef` for ref forwarding
- Exported prop types for all components:
  - `ActorAvatarProps`
  - `BaseAvatarProps`
  - `DocIntegrationAvatarProps`
  - `OrganizationAvatarProps`
  - `ProjectAvatarProps`
  - `SentryAppAvatarProps`
  - `TeamAvatarProps`
  - `UserAvatarProps`
  - `GravatarProps`
  - `LetterAvatarProps`

### Code Improvements
- Consolidated avatar component styles in `baseAvatarComponentStyles.tsx`
- Removed inline `BackgroundAvatar` component, integrated into `BaseAvatar`
- Fixed `SentryAppAvatar` and `ProjectAvatar` implementations
- Updated ~200 import statements across the codebase

### Documentation
- Added Storybook stories for all avatar types (User, Team, Project, Organization, SentryApp, DocIntegration)

## Implementation Details

- `BaseAvatar` now handles all avatar types (upload, gravatar, letter_avatar, background)
- Extracted reusable styles to `BaseAvatarComponentStyles`
- Improved error handling and fallback rendering
- Better TypeScript type inference throughout

## Migration Path
Old imports remain functional via deprecation wrappers:
```typescript
// Old (still works)
import UserAvatar from 'sentry/components/avatar/userAvatar';

// New
import {UserAvatar} from 'sentry/components/core/avatar/userAvatar';
```