# Refactor route functions in BaseService

Extract route helper functions (`_makeFullUrl`, `_regex`, `_regexFromPath`, `_namedParamsForMatch`) from BaseService into standalone, testable functions in new `route.js` module.