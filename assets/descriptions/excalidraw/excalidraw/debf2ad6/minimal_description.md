# Refactor: Remove dependency on static Scene

Remove static `Scene` methods (`Scene.getScene()`, `Scene.mapElementToScene()`) and pass `scene` or `elementsMap` explicitly throughout the codebase instead of relying on global lookups.