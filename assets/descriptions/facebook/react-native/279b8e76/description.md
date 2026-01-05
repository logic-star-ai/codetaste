Title
-----
Flatten `Animated` directory structure by removing legacy `src/` subdirectory

Summary
-------
The `Libraries/Animated/` module currently has an unnecessary `src/` subdirectory (`Libraries/Animated/src/`). This refactoring collapses the directory structure by moving all files from `Animated/src/` up one level to `Animated/` and updating all import paths accordingly.

Why
---
- Legacy `react-animated` package is no longer needed
- Extra `src/` nesting adds unnecessary complexity
- Simplifies module structure and import paths
- Aligns with standard React Native library organization

Changes
-------
- Move all files from `Libraries/Animated/src/*` → `Libraries/Animated/*`
  - Core files: `Animated.js`, `AnimatedEvent.js`, `AnimatedImplementation.js`, etc.
  - Subdirectories: `animations/`, `components/`, `nodes/`, `polyfills/`
  - Test files: `__tests__/`
- Update all import paths from `...Animated/src/...` → `...Animated/...`
  - Within `Animated/` module itself (relative imports like `../../Utilities/...` → `../Utilities/...`)
  - In consuming modules (`ScrollView`, `TouchableOpacity`, `LogBox`, etc.)
  - In root `index.js`
- Remove legacy `react-animated` release package artifacts:
  - `Libraries/Animated/release/` directory
  - `Libraries/Animated/examples/` directory