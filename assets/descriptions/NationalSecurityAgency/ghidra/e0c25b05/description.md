Title
-----
Refactor JLabel → GLabel variants, JComboBox → GComboBox, update renderers

Summary
-------
Replace generic Swing components with specialized Ghidra variants to make HTML rendering behavior explicit and eliminate repetitive renderer configuration code.

Why
---
- Current code relies on `DockingUtils.createNonHtmlLabel()` / `createHtmlLabel()` factory methods scattered throughout
- HTML rendering behavior is not type-safe or explicit at the type level
- Requires manual calls to `turnOffHTMLRendering()` which are easy to forget
- Difficult to distinguish mutable vs immutable labels at usage sites
- Renderers need explicit HTML configuration in many places

What Changed
------------
**New Label Types:**
- `GLabel` - Immutable, non-HTML label (replaces `createNonHtmlLabel()`)
- `GDLabel` - Mutable/Dynamic, non-HTML label  
- `GHtmlLabel` - Immutable, HTML-enabled label (replaces `createHtmlLabel()`)
- `GDHtmlLabel` - Mutable/Dynamic, HTML-enabled label
- `GIconLabel` - Icon-only label

**Component Replacements:**
- Replace `JComboBox` → `GComboBox` (with HTML rendering disabled by default)
- Replace `DockingUtils.createNonHtmlLabel(...)` → `new GLabel(...)` / `new GDLabel(...)`
- Replace `DockingUtils.createHtmlLabel(...)` → `new GHtmlLabel(...)` / `new GDHtmlLabel(...)`
- Remove redundant `DockingUtils.turnOffHTMLRendering()` calls

**Renderer Updates:**
- Update cell renderers to use new label types
- Remove explicit HTML disabling where now handled by component type
- Update `GListCellRenderer`, `GTableHeaderRenderer`, etc.

**Helper Additions:**
- `ResourceManager.loadImages(String...)` - bulk icon loading
- `HTMLUtilities.escapeHTML(String)` - explicit HTML escaping

**Pattern:**
- Use `GLabel` for static text (constructor-only)
- Use `GDLabel` when `setText()` will be called  
- Use `GHtmlLabel` / `GDHtmlLabel` for HTML content
- Use `GIconLabel` for icon-only labels

Scope
-----
- ~200+ files affected across Features/Base, Framework/Docking, etc.
- All usages of `createNonHtmlLabel()` / `createHtmlLabel()` in Ghidra codebase
- Dialog panels, status bars, table/list/tree renderers, filter panels, editors
- Merge dialogs, data type management, function editors, memory dialogs, etc.