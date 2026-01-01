# Refactor: Migrate Functional Tests to `@prestashop-core/ui-testing` (Part 1)

## Summary

Migrate functional tests to use `@prestashop-core/ui-testing` library instead of local page objects. This refactoring consolidates page object models into a centralized testing library and updates all affected test files accordingly.

## Scope

**Test Categories:**
- Audit tests (`BO/02_orders`, `BO/03_catalog`, `BO/04_customers`)
- API endpoint tests (`09_product/*`)
- Order management tests (`BO/02_orders/01_orders/createOrders/*`, `viewAndEditOrder/*`)
- Invoice tests (`BO/02_orders/02_invoices/*`)
- Dashboard tests (`BO/01_dashboard/*`)
- Login tests (`BO/00_login/*`)

## Changes

### Import Migration

Replace local page object imports:
```diff
- import addOrderPage from '@pages/BO/orders/add';
- import createProductsPage from '@pages/BO/catalog/products/add';
- import addCustomerPage from '@pages/BO/customers/add';
+ import {
+   boOrdersCreatePage,
+   boProductsCreatePage,
+   boCustomersCreatePage,
+ } from '@prestashop-core/ui-testing';
```

### Page Object Renaming

Update references throughout test files:
- `addOrderPage` → `boOrdersCreatePage`
- `createProductsPage` / `addProductPage` → `boProductsCreatePage`
- `addCustomerPage` → `boCustomersCreatePage`
- `invoicesPage` → `boInvoicesPage`
- `creditSlipsPage` → `boCreditSlipsPage`
- `deliverySlipsPage` → `boDeliverySlipsPage`
- `addAttributePage` → `boAttributesCreatePage`
- `combinationsTab` → `boProductsCreateTabCombinationsPage`
- ... (similar pattern for other page objects)

### Deleted Files

Remove local page object implementations:
- `tests/UI/pages/BO/orders/add.ts`
- `tests/UI/pages/BO/orders/invoices/index.ts`
- `tests/UI/pages/BO/orders/creditSlips/index.ts`
- `tests/UI/pages/BO/orders/deliverySlips/index.ts`
- `tests/UI/pages/BO/catalog/products/add/*.ts`
- `tests/UI/pages/BO/customers/add.ts`
- ... (other migrated page objects)

## Why

- **Centralization**: Single source of truth for page object models
- **Maintainability**: Reduce duplication across test suites
- **Reusability**: Share page objects across different test projects
- **Consistency**: Standardized naming conventions (`bo*` prefix pattern)

## Testing

✅ CI validation required  
✅ All functional tests must pass with new imports

---

**Note**: This is Part 1 of the migration. Additional page objects will be migrated in subsequent PRs.