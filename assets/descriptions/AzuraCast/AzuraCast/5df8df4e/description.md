# Migrate from Vuelidate to Regle for Frontend Form Validation

## Summary
Replace Vuelidate validation library with Regle across entire frontend codebase to modernize form validation approach and improve TypeScript integration.

## Why
- Better TypeScript support and type inference
- Improved integration with Vue 3 Composition API + Pinia
- More maintainable validation API
- Eliminates custom wrapper functions (`useVuelidateOnForm`, `useVuelidateOnFormTab`)
- Modern validation library architecture

## Dependencies Changed
- **Removed**: `@vuelidate/core`, `@vuelidate/validators`
- **Added**: `@regle/core`, `@regle/rules`, `pinia`

## Global Changes
- Created centralized `vendor/regle.ts` configuration w/ localized validation messages
- Validation state accessor changed: `v$` → `r$`
- ESLint: Disabled `@typescript-eslint/unbound-method` rule

## Validation Utilities
**Removed**:
- `functions/useVuelidateOnForm.ts`
- `functions/useVuelidateOnFormTab.ts`

**Added**:
- `functions/useFormTabClass.ts`
- Form stores using Pinia for complex forms (Admin Settings, Stations, Webhooks, etc.)
- Scoped validation with `useAppScopedRegle` / `useAppCollectScope`

## Custom Validation Rules
Migrated to Regle format:
- `isValidPassword` (wraps existing `validatePassword` function)
- `isValidHexColor` (hex color validation)
- All rules wrapped with localized error messages

## Component Updates

### Account Components
- `ApiKeyModal.vue`, `ChangePasswordModal.vue`, `EditModal.vue`
- `PasskeyModal.vue`, `TwoFactorModal.vue`
- Removed `Account/EditForm.vue` (inlined into modal)

### Admin Components
- **Backups**: `ConfigureModal.vue`, `RunBackupModal.vue`
- **Branding**: `BrandingForm.vue`
- **Custom Fields**: `EditModal.vue` (removed separate `Form.vue`)
- **Permissions**: `EditModal.vue`, form components (introduced validation scoping)
- **Settings**: Complete refactor using Pinia store (`form.ts`)
  - `GeneralTab.vue`, `SecurityPrivacyTab.vue`, `ServicesTab.vue`
  - `TestMessageModal.vue`
- **Stations**: Complete refactor using Pinia store (`Form/form.ts`)
  - All tab forms: Profile, Frontend, Backend, HLS, Requests, Streamers, Admin
  - `CloneModal.vue` (removed `CloneModalForm.vue`)
- **Storage Locations**: `EditModal.vue`, refactored with Pinia store

### Station Components
- **Mounts**: `EditModal.vue` (using Pinia store)
- **Playlists**: All forms + `EditModal.vue` (using scoped validation)
- **Podcasts**: Branding form, category form, episode edit
- **Remotes**: `EditModal.vue` + forms (using Pinia store)
- **SFTP Users**: `EditModal.vue` (removed separate `Form.vue`)
- **Streamers**: `EditModal.vue` + forms (using Pinia store + scoped validation)
- **Webhooks**: Complete refactor
  - All webhook type forms (Discord, Email, Generic, Mastodon, Telegram, etc.)
  - Centralized form store in `Form/form.ts` with type-specific configs
  - Validation scoping for tab forms

### Form Components
- `FormGroupCheckbox.vue`, `FormGroupField.vue`, `FormGroupMultiCheck.vue`
- Updated to work with Regle's validation structure

## Base Edit Modal
Refactored `useBaseEditModal.ts`:
- Removed Vuelidate dependencies
- Signature changed: now accepts `form` ref, `resetForm` callback, and optional `validateForm` callback
- No longer manages form state internally
- Simpler validation flow

## API/Backend Updates
- Minor OpenAPI schema updates (type clarifications)
- `PodcastBrandingConfiguration` schema definition
- `StorageLocation.s3UsePathStyle` typing fix

## Migration Pattern
```typescript
// Before (Vuelidate)
const {form, v$, resetForm, ifValid} = useVuelidateOnForm(
    {name: {required}},
    {name: ''}
);

// After (Regle)
const {record: form, reset: resetForm} = useResettableRef({name: ''});
const {r$} = useAppRegle(form, {name: {required}}, {});
```

## Form State Management
Complex forms (Settings, Stations, Webhooks, Remotes, Streamers) now use Pinia stores for:
- Centralized form state
- Validation rules
- Validation groups (for tabbed forms)
- Reset logic

## Testing Notes
- All form validation behavior should remain functionally identical
- Error messages localized and consistent
- Tab validation indicators work via `useFormTabClass`
- Async validation properly awaited: `(await r$.$validate()).valid`