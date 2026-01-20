# Refactor middleware and reducer loading to be explicit

Move from implicit to explicit loading of middlewares and reducers. Currently, each feature's `index.js` imports its own middleware/reducer files, causing circular dependencies and platform-specific code leaking across web/native boundaries. Consolidate all imports into platform-specific entry points.