# Remove old IE compatibility mode logic, switch to native types instead

## Summary
Remove `@ephox/sand` wrapper functions/constructors for browser APIs and replace with native JavaScript/DOM types. This eliminates compatibility shims that were required for older IE versions.

## Why
- Old IE compatibility layers are no longer necessary
- Native browser APIs (JSON, XMLHttpRequest, Blob, etc.) are now universally supported
- Reduces bundle size and complexity
- Improves code clarity and maintainability

## Changes

### Removed `@ephox/sand` wrappers
- ❌ `JSON.ts` → ✅ Native `JSON` global
- ❌ `XMLHttpRequest.ts` → ✅ Native `XMLHttpRequest` constructor
- ❌ `FileReader.ts` → ✅ Native `FileReader` constructor  
- ❌ `Blob.ts` → ✅ Native `Blob` constructor
- ❌ `URL.ts` → ✅ Native `URL` API from `@ephox/dom-globals`
- ❌ `Uint8Array.ts` → ✅ Native `Uint8Array` constructor
- ❌ `Window.ts` (atob, requestAnimationFrame) → ✅ Native globals
- ❌ `FormData.ts`, `Event.ts`, `XMLSerializer.ts`, `NodeFilter.ts`

### Updated imports
```diff
- import { JSON as Json } from '@ephox/sand';
+ // Use native JSON directly

- import { XMLHttpRequest } from '@ephox/sand';
+ import { XMLHttpRequest } from '@ephox/dom-globals';

- import { URL } from '@ephox/sand';
+ import { URL } from '@ephox/dom-globals';
```

### Updated usage patterns
```diff
- Json.stringify(...) → JSON.stringify(...)
- XMLHttpRequest() → new XMLHttpRequest()
- FileReader() → new FileReader()
- Blob(...) → new Blob(...)
- Uint8Array(...) → new Uint8Array(...)
- Window.atob(...) → atob(...)
```

### Modules affected
- `modules/agar/...`
- `modules/alloy/...`
- `modules/boulder/...`
- `modules/imagetools/...`
- `modules/mcagar/...`
- `modules/sand/...` (gutted, only exports `HTMLElement`, `Node`, `PlatformDetection`)
- `modules/sugar/...`
- `modules/tinymce/...` (core, plugins: image, imagetools, paste, quickbars; theme: silver)