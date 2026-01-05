# Refactor / rename Billing object classes to match SQL schema

## Summary

Rename billing classes to align with SQL table names and split nested classes into separate top-level classes. Update all references throughout codebase.

## Changes

**Class Renaming**
- `BillingEvent` (base class) → `BillingBase` (superclass for all billing types)
- `BillingEvent.OneTime` → `BillingEvent` (top-level)
- `BillingEvent.Recurring` → `BillingRecurrence` (top-level)
- `BillingEvent.Cancellation` → `BillingCancellation` (top-level)

**Enum Relocation**
- Move `Flag`, `Reason`, `RenewalPriceBehavior` from `BillingEvent` to `BillingBase`

**Pipeline/Action Renaming**
- `ExpandRecurringBillingEventsAction` → `ExpandBillingRecurrencesAction`
- `ExpandRecurringBillingEventsPipeline` → `ExpandBillingRecurrencesPipeline`
- Update all related method names, paths, and metadata files

**Variable/Method Updates**
- `recurring` → `billingRecurrence` / `recurrence`
- `oneTime` → `billingEvent`
- `getOneTimeBillingEvent()` → `getBillingEvent()`
- `getRecurringBillingEvent()` → `getBillingRecurrence()`
- `recurringEventHistoryRevisionId` → `recurrenceHistoryRevisionId`
- ... (similar patterns throughout)

## Scope

- [x] Core model classes
- [x] Flow implementations (domain create/renew/transfer/delete/update/...)
- [x] Beam pipeline and invoicing logic
- [x] Test files and fixtures
- [x] XML configuration files (web.xml, cloud-scheduler-tasks.xml)
- [x] Documentation and comments
- [x] Database schema references
- [x] Build configuration (gradle)

## Rationale

- Align class names with SQL table naming conventions
- Use `BillingBase` as superclass name (since one-time events are now called `BillingEvent`)
- Improve code clarity by using separate top-level classes instead of nested classes