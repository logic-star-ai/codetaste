# Rename runtime APIs to snake_case

## Summary
Refactor all exposed runtime APIs from camelCase to snake_case with underscore prefixes for improved readability and consistency.

## Why
- Better visual separation and readability of runtime function names
- More consistent naming convention across the runtime
- Clearer distinction between internal runtime APIs (prefixed with `_`) and user code

## Changes

### Core Runtime Functions
- `createTemplate` → `_template`
- `createRenderer` / `createContent` → `_content_branch` / `_content`
- `registerContent` → `_content_resume`
- `localClosures` → `_content_closures`

### Signal Functions
- `state` → `_let`
- `value` → `_const`
- `effect` → `_script`
- `intersection` → `_or`
- `dynamicClosure` → `_closure`
- `dynamicClosureRead` → `_closure_get`
- `loopClosure` → `_for_closure`
- `conditionalClosure` → `_if_closure`

### Control Flow
- `conditional` → `_if`
- `loopOf` / `loopIn` / `loopTo` → `_for_of` / `_for_in` / `_for_to`
- `dynamicTag` → `_dynamic_tag`
- `awaitTag` → `_await`
- `createTry` → `_try`

### DOM Manipulation
- `attr` → `_attr`
- `data` → `_text`
- `textContent` → `_text_content`
- `on` → `_on`
- `html` → `_html`
- `classAttr` / `styleAttr` → `_attr_class` / `_attr_style`
- `classItem` / `styleItem` → `_attr_class_item` / `_attr_style_item`
- `attrs` / `attrsEvents` → `_attrs` / `_attrs_script`
- `partialAttrs` → `_attrs_partial`
- ...

### HTML/SSR Functions
- `escapeXML` → `_escape`
- `write` / `writeTrailers` → `_html` / `_trailers`
- `writeScope` → `_scope`
- `writeEffect` → `_script`
- `nextScopeId` → `_scope_id`
- `markResumeNode` → `_el_resume`
- `resumeConditional` → `_if`
- `fork` → `_await`
- ...

### Utility Functions
- `register` → `_resume`
- `nodeRef` → `_el`
- `nextTagId` → `_id`
- `setTagVar` → `_var`
- `tagVarSignal` → `_return`
- `getAbortSignal` / `resetAbortSignal` → `$signal` / `$signalReset`
- `hoist` → `_hoist`
- `enableCatch` → `_enable_catch`
- ...

### Generated Identifier Patterns
- Effect suffixes: `_effect` → `__script`
- Setup prefixes: `$setup$...` → `$...__setup`
- Expression prefixes: `$expr_...` → `$...__OR__...`
- Closure suffixes: `_closure` → `__closure`
- Double underscore (`__`) for compound identifier segments