# Refactor generator modules to eliminate side effects

Restructure generator modules to:
- Move `LangGenerator` class definitions from `generators/lang.js` → `generators/lang/lang_generator.js`
- Move entrypoints from `generators/lang/all.js` → `generators/lang.js`
- Make block generator modules (`generators/lang/*.js`) side-effect-free by exporting individual functions
- Create and configure `langGenerator` instances in the entrypoint files