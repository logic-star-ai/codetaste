# Title
Remove Element Plus dependency and migrate to custom UI components

# Summary
Replace Element Plus with lightweight alternatives and custom components to reduce bundle size and improve customization.

# Motivation
- Reduce dependency on heavy UI framework
- Improve bundle size and performance
- Enable better theming and customization
- Use modern, composable UI components

# Changes

## Dependencies Removed
- `element-plus` package
- `@element-plus/icons-vue` package
- Related type definitions (`@types/lodash`, `@types/lodash-es`)
- Transitive deps: `async-validator`, `@ctrl/tinycolor`, `memoize-one`, `normalize-wheel-es`, etc.

## Dependencies Added
- `vue-sonner` for toast notifications
- `vue-pick-colors` for color picker
- Custom UI components (shadcn-vue style)

## Component Replacements
- `ElMessage` → `toast()` from vue-sonner
- `ElMessageBox` → `AlertDialog` component
- `ElColorPicker` → `PickColors` from vue-pick-colors
- `ElIcon` → `lucide-vue-next` icons
- `ElTabs` → Custom `Tabs` components
- `ElForm`/`ElFormItem` → Custom `FormItem` component
- `ElInput` → Custom `Input` component
- `ElButton` → Custom `Button` component
- `ElSwitch` → Custom `Switch` component
- `ElCol`/`ElRow` → CSS Grid/Flexbox
- `ElUpload` → Custom drag-and-drop with `useFileDialog`
- `ElInputNumber` → Custom `NumberField` component
- `ElSelect` → Custom `Select` component

## Style Updates
- Replace Element Plus CSS variables with HSL-based custom properties
- `var(--el-text-color-regular)` → `hsl(var(--foreground))`
- `var(--el-bg-color)` → `hsl(var(--background))`
- Remove Element Plus theme imports
- Clean up Element Plus-specific style fixes

## File Changes
- Remove `src/element/index.ts` plugin file
- Update `main.ts` to remove Element Plus registration
- Refactor 15+ component files
- Add new UI primitives in `src/components/ui/...`
- Add `CustomUploadForm.vue` and `FormItem.vue` helpers

# Implementation Details
- Custom components follow Radix Vue + Tailwind pattern
- Use composables like `useFileDialog`, `useVModel` for functionality
- Maintain existing features while improving DX
- CodeMirror integration for custom code editor preserved