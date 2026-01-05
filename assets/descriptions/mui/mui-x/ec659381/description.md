# Simplify field hooks API

## Summary
Refactor field hooks (`useDateField`, `useTimeField`, `useDateTimeField`, range field hooks) and `useClearableField` to provide a simpler, more intuitive API with less boilerplate.

## Current Issues
- Field hooks require `{ props, inputRef }` object instead of direct props
- `useClearableField` takes multiple separate parameters (`fieldProps`, `InputProps`, `clearable`, `onClear`, `slots`, `slotProps`)
- Developers must manually extract/destructure `ref`, `InputProps`, `clearable`, `onClear` from field response
- Multi-input range fields require passing `startInputRef`/`endInputRef` separately
- Ref naming is inconsistent (`ref` for input element is ambiguous)

## Proposed Changes

**Field Hooks:**
- Accept props directly: `useDateField(props)` instead of `useDateField({ props, inputRef })`
- Rename returned `ref` → `inputRef` for clarity
- Include `inputRef` in props (no separate parameter)
- Remove `startInputRef`/`endInputRef` params from multi-input range hooks

**`useClearableField`:**
- Accept single props object instead of multiple params
- Return complete processed props (not split into `InputProps` + `fieldProps`)
- Enable direct spreading: `useClearableField(fieldResponse)` → `<TextField {...result} />`

**Types:**
- Remove `Use*FieldParams` interfaces (no longer needed)
- Move `FieldSlots`/`FieldSlotProps` → `UseClearableFieldSlots`/`UseClearableFieldSlotProps`
- Add `convertFieldResponseIntoMuiTextFieldProps` utility

## Example

```tsx
// Before
const { inputRef: externalInputRef, ...textFieldProps } = props;
const { ref, onClear, clearable, InputProps, ...fieldProps } = useDateField({ 
  props: textFieldProps, 
  inputRef: externalInputRef 
});
const { InputProps: ProcessedInputProps, fieldProps: processedFieldProps } = useClearableField({
  fieldProps, InputProps, clearable, onClear, slots, slotProps
});
return <TextField {...processedFieldProps} InputProps={ProcessedInputProps} inputProps={{ ref }} />;

// After
const fieldResponse = useDateField(props);
const processedProps = useClearableField({ ...fieldResponse, slots, slotProps });
return <TextField {...processedProps} />;
```

## Migration
Provide migration guide for... custom field implementations using hooks directly.