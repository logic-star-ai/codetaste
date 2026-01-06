# Move spec helper modules to `spec/lib` subdirectory

Reorganize test helper modules by moving them from `spec/` root into `spec/lib/`:
- `events-helpers.ts`
- `screen-helpers.ts`
- `spec-helpers.ts`
- `video-helpers.js`
- `window-helpers.ts`

Update all import statements across spec files from `./helpers` → `./lib/helpers`