# Remove obsolete `entryComponents` declarations

## Summary
Remove all `entryComponents` usages across the codebase since they're no longer necessary with Ivy.

## Changes

**Test Files**
- Remove test-specific `NgModule`s that only existed as workaround for angular/angular#10760
- Move component declarations directly into `TestBed.configureTestingModule()`
- Clean up unnecessary `NgModule` imports

**Example Modules**  
- Strip `entryComponents` arrays from all `@NgModule` decorators in `src/components-examples/*`

**Affected Areas**
- CDK: dialog, overlay (dispatchers, position, scroll), portal, scrolling
- Material: bottom-sheet, datepicker, dialog, snack-bar
- Material Experimental: mdc-dialog, mdc-snack-bar, mdc-table, ...
- All component examples

## Why
With Ivy, Angular automatically determines which components are entry components through static analysis, making manual `entryComponents` declarations obsolete and unnecessary.