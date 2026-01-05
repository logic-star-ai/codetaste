# Title

Rename import assertion AST nodes to import attribute

# Summary

Rename all AST nodes, fields, methods, and syntax kinds related to import assertions to use "attribute" terminology instead of "assertion" throughout the JavaScript parser and related modules.

# Why

The `assert` keyword for import attributes was previously removed in favor of the standardized `with` keyword. However, the internal AST representation still uses "assertion" terminology, which is now inconsistent with the actual syntax being parsed.

# Changes

**AST Node Renames:**
- `JsImportAssertion` → `JsImportAttribute`
- `JsImportAssertionEntry` → `JsImportAttributeEntry`  
- `JsImportAssertionEntryList` → `JsImportAttributeEntryList`
- `AnyJsImportAssertionEntry` → `AnyJsImportAttributeEntry`
- `JsBogusImportAssertionEntry` → `JsBogusImportAttributeEntry`

**Method/Field Renames:**
- `.assertion()` → `.attribute()`
- `.assertions` → `.attributes`
- `.with_assertion()` → `.with_attribute()`

**Syntax Kind Renames:**
- `JS_IMPORT_ASSERTION` → `JS_IMPORT_ATTRIBUTE`
- `JS_IMPORT_ASSERTION_ENTRY` → `JS_IMPORT_ATTRIBUTE_ENTRY`
- `JS_IMPORT_ASSERTION_ENTRY_LIST` → `JS_IMPORT_ATTRIBUTE_ENTRY_LIST`
- `JS_BOGUS_IMPORT_ASSERTION_ENTRY` → `JS_BOGUS_IMPORT_ATTRIBUTE_ENTRY`

# Scope

Affected modules:
- `biome_js_parser` - parsing logic
- `biome_js_syntax` - AST definitions, node types, kind enums
- `biome_js_factory` - node factory functions
- `biome_js_formatter` - formatting rules for import/export statements
- `biome_js_analyze` - lint rules using import attributes
- Test snapshots (`.rast` files)
- Grammar definition (`js.ungram`)

# Notes

This is a **breaking change** that affects the public AST API.