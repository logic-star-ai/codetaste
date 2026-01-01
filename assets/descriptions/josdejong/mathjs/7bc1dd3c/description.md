# Title
-----
Reorganize utils functions and migrate to ES6 import/export

# Summary
-------
Consolidate scattered utility functions into logical modules and migrate from CommonJS to ES6 module syntax.

# Changes
---------

### Collection utilities consolidation
- Merge `deepMap`, `deepForEach`, `reduce`, `scatter`, `containsCollections` into single `utils/collection.js` file
- Export as named exports

### BigNumber bitwise operations consolidation  
- Merge `bitAnd`, `bitNot`, `bitOr`, `bitXor`, `leftShift`, `rightArithShift` into `utils/bignumber/bitwise.js`
- Export as named exports

### Function renaming for clarity
- `array.size` → `array.arraySize` (avoid confusion with matrix.size())
- `object.map` → `object.mapObject` (avoid confusion with Array.map)

### Cleanup
- Delete `utils/boolean.js`, move `isBoolean` to `utils/is.js`
- Delete individual collection/bignumber files after consolidation

### ES6 migration
- Replace `require()` with `import` statements
- Replace `module.exports` with `export` declarations  
- Use named exports throughout
- Update all import paths and references

# Benefits
----------
- Fewer files, better organization
- Related functions grouped together
- Modern, consistent module syntax
- Clearer function naming conventions