# refactor(material/core): reduce mixin function boilerplate

## Summary
Remove unnecessary `*Ctor` type interfaces and intermediate base classes for mixins throughout Angular Material components. TypeScript now correctly infers mixin types without explicit annotations.

## Why
- `CanColorCtor`, `CanDisableCtor`, `CanDisableRippleCtor`, `HasTabIndexCtor`, etc. are no longer necessary
- TS type inference handles mixin types correctly without manual declarations
- Reduces boilerplate and simplifies mixin usage

## Changes

### Remove explicit type annotations
**Before:**
```typescript
class MatButtonBase {
  constructor(public _elementRef: ElementRef) {}
}
const _MatButtonMixinBase: CanColorCtor & CanDisableCtor & typeof MatButtonBase = 
    mixinColor(mixinDisabled(MatButtonBase));
```

**After:**
```typescript
const _MatButtonBase = mixinColor(mixinDisabled(class {
  constructor(public _elementRef: ElementRef) {}
}));
```

### Deprecate `*Ctor` interfaces
Mark as `@deprecated` with breaking change notice for v13.0.0:
- `CanColorCtor`
- `CanDisableCtor` 
- `CanDisableRippleCtor`
- `HasTabIndexCtor`
- `HasInitializedCtor`
- `CanUpdateErrorStateCtor`

### Components affected
- `material/button`
- `material/checkbox`
- `material/chips`
- `material/datepicker`
- `material/form-field`
- `material/icon`
- `material/input`
- `material/list`
- `material/menu`
- `material/paginator`
- `material/progress-bar`
- `material/progress-spinner`
- `material/radio`
- `material/select`
- `material/slide-toggle`
- `material/slider`
- `material/sort`
- `material/stepper`
- `material/tabs`
- `material/toolbar`
- `material/tree`
- `material-experimental/mdc-*` variants