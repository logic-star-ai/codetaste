# Remove `util` from global scope and convert to proper module

Convert `util.js` from a globally-accessible module (`window.util`) to a leaf module that must be explicitly imported via `require()` everywhere it's used.