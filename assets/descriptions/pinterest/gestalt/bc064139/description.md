# Title
Migrate TextField, Module, Upsell, ActivationCard examples to Sandpack

## Summary
Refactor documentation examples for TextField, Module, Upsell, and ActivationCard components to use Sandpack interactive code editor instead of inline code strings.

## Why
- **Better organization**: Examples scattered as inline template strings → dedicated files in `docs/examples/`
- **Maintainability**: Easier to update, test, and reuse examples
- **User experience**: Interactive Sandpack editor vs. static code blocks
- **Consistency**: Align with existing Sandpack-based documentation pattern

## Changes
### Structure
- Extract ~40+ inline examples to separate `.js` files under:
  - `docs/examples/activationcard/...`
  - `docs/examples/module/...`
  - `docs/examples/textfield/...`
  - `docs/examples/upsell/...`

### Component updates
- Replace `defaultCode={...}` props with `sandpackExample={<SandpackExample />}`
- Import example files at page level
- Update PageHeader to use SandpackExample for main examples
- Reorganize sections for better flow

### Examples migrated
**ActivationCard**: mainExample, completeVariant, needsAttentionVariant, notStartedVariant, pendingVariant

**Module**: mainExample, staticVariant, expandable, expandableGroup, exampleWithExternalControl, ...with icon/badge/error/iconButton variants

**TextField**: ~25+ examples including labels, validation, mobile keyboard, maxLength, tags, password, disabled, readonly, error messages, best practices (do/don't pairs)

**Upsell**: mainExample, textVariant, iconVariant, imageVariant, actionsVariant, singleTextField, multipleTextField, best practices

## Implementation
- ✅ Create example files with proper Flow types
- ✅ Update page imports and component structure  
- ✅ Replace inline code with SandpackExample component
- ✅ Configure layout/preview height per example
- ✅ Maintain accessibility examples and best practices