# Rename TinyMCE core modules that conflict with native DOM names

## Summary
Rename internal TinyMCE types and classes that conflict with native DOM/TypeScript types to avoid naming collisions. Keep filenames and exported variable names unchanged for backwards compatibility.

## Why
- TinyMCE modules (`Node`, `Selection`, `TreeWalker`, `Serializer`) conflict with TypeScript's native DOM type names
- Causes aliasing issues and type ambiguity when working with dom-globals
- Cannot be renamed publicly, so internal refactoring is needed

## What Changed
Renamed the following internal types/classes while preserving exported names:

* `Node` → `AstNode` (html/Node.ts)
* `Selection` → `EditorSelection` (dom/Selection.ts)  
* `TreeWalker` → `DomTreeWalker` (dom/TreeWalker.ts)
* `Serializer` → `DomSerializer` (dom/Serializer.ts)
* `Serializer` → `HtmlSerializer` (html/Serializer.ts)
* `DomSerializer` → `DomSerializerImpl` (dom/DomSerializerImpl.ts)

## Scope
- Updated all internal imports and type references across core modules
- Updated type signatures, interfaces, and variable declarations
- Removed remaining aliasing of dom globals
- Tests updated to use new names

## Notes
- Filenames remain unchanged
- Public API exports remain unchanged  
- Only internal class names, types, and variable names modified
- Eliminates last of dom global aliasing issues