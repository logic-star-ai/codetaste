# Rename hand-detection package to hand-pose-detection

## Summary
Rename the `hand-detection` package to `hand-pose-detection` across the entire codebase, including directory structure, package names, imports, and documentation.

## Why
The name `hand-detection` implies bounding box detection only, which doesn't accurately convey that the package performs **pose detection** (keypoint estimation). The new name `hand-pose-detection` better reflects the actual functionality.

## Changes Required

### Directory & Package Structure
- Rename `hand-detection/` → `hand-pose-detection/`
- Update `package.json`: `@tensorflow-models/hand-detection` → `@tensorflow-models/hand-pose-detection`
- Update package distribution files: `hand-detection.js` → `hand-pose-detection.js` (+ `.min.js`, `.esm.js`)
- Update global namespace: `handDetection` → `handPoseDetection`

### Code Updates
- Update all import statements: `@tensorflow-models/hand-detection` → `@tensorflow-models/hand-pose-detection`
- Update variable names in examples/demos from `handdetection` → `handPoseDetection`
- Update test names and identifiers

### Documentation
- Update all README files to reference `hand-pose-detection`
- Update demo URLs: `.../demos/hand-detection/...` → `.../demos/hand-pose-detection/...`
- Update GitHub links in documentation
- Update descriptions: "hand detection" → "hand pose detection"

### Build Configuration
- Update `rollup.config.js` package name
- Update `cloudbuild.yml` directory references
- Update demo `package.json` files

## Files Affected
- All files in `hand-detection/` directory (rename to `hand-pose-detection/`)
- Package manifests, build configs, demos, source code, tests, documentation