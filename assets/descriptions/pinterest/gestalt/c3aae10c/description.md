# Docs: Migrate component examples to Sandpack

## Summary

Migrate documentation examples for **Tooltip**, **SelectList**, **List**, **TapArea**, **DataPoint**, and **Divider** components from inline code strings to Sandpack interactive examples.

## Changes

- Extract all inline example code to separate `.js` files in `docs/examples/[component]/`
- Replace `defaultCode={...}` props with `sandpackExample={<SandpackExample />}` components
- Add appropriate Sandpack configuration (layout, hideEditor, hideControls, previewHeight, etc.)
- Improve example organization and reusability

## Components affected

- **DataPoint**: 12 examples extracted (main, size variants, trend examples, localization, best practices)
- **Divider**: 11 examples extracted (orientation, usage patterns, do/don't examples)
- **List**: 17 examples extracted (types, nesting, spacing, labels, composition)
- **SelectList**: 13 examples extracted (sizes, grouping, controlled, validation, accessibility)
- **TapArea**: 7 examples extracted (basic, roles, accessibility, ref, inline usage)
- **Tooltip**: 11 examples extracted (positioning, z-index, accessibility, usage patterns)

## Benefits

- Enables interactive code editing in documentation
- Improves code maintainability and reusability
- Separates example code from documentation markup
- Provides consistent Sandpack experience across components
- Allows better control over example presentation (editor visibility, preview size, etc.)

## Technical details

- All example files follow standard pattern: `export default function Example(): Node { ... }`
- Uses Flow strict mode
- Sandpack examples configured per use case (column/row layout, editor/control visibility)
- Minor layout adjustments for optimal presentation (cardSize, previewHeight)