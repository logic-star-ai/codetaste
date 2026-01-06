# Consolidate `ui/utils` into `utils` to remove `ui/` folder

Move remaining utility files from `packages/components/src/ui/utils/` to `packages/components/src/utils/` and update all imports across the codebase. This completes the removal of the `ui/` folder structure (started in #52953).