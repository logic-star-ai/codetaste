# Migrate Functional Tests to `@prestashop-core/ui-testing` (Part 2)

## Summary

Migrate functional tests to use page objects from the centralized `@prestashop-core/ui-testing` package instead of local implementations. This refactoring removes local page object files and updates test imports to use the shared package.

## Why

- **Consolidate page objects** into a centralized, reusable package
- **Improve maintainability** by having a single source of truth for page objects
- **Enhance reusability** across different test suites and projects
- **Reduce code duplication** by removing local implementations

## Scope

### Back Office (BO) Pages Migrated

**Catalog**
- `monitoring` → `boMonitoringPage`
- `discounts` → `boCartRulesPage`
- `discounts/add` → `boCartRulesCreatePage`

**Customers**
- `addresses` → `boAddressesPage`
- `addresses/add` → `boAddressesCreatePage`
- `view` → `boCustomersViewPage`

**Customer Service**
- `customerService` → `boCustomerServicePage`
- `orderMessages` → `boOrderMessagesPage`
- `merchandiseReturns` → `boMerchandiseReturnsPage`
- `merchandiseReturns/edit` → `boMerchandiseReturnsEditPage`

**Orders**
- `shoppingCarts/view` → `boShoppingCartsViewPage`
- `view/customerBlock` → `boOrdersViewBlockCustomersPage`
- `view/messagesBlock` → `boOrdersViewBlockMessagesPage`
- `view/paymentBlock` → `boOrdersViewBlockPaymentsPage`
- `view/viewOrderBasePage` → `boOrdersViewBasePage`

**Other**
- `stats` → `boStatisticsPage`
- `modules/productComments` → `modProductCommentsBoMain`

### Front Office (FO) Pages Migrated

**Classic Theme - My Account**
- `orderHistory` → `foClassicMyOrderHistoryPage`
- `orderDetails` → `foClassicMyOrderDetailsPage`
- `merchandiseReturns` → `foClassicMyMerchandiseReturnsPage`
- `addresses/add` → `foClassicAddressesCreatePage`

**Hummingbird Theme - My Account**
- `orderHistory` → `foHummingbirdMyOrderHistoryPage`
- `orderDetails` → `foHummingbirdMyOrderDetailsPage`
- `merchandiseReturns` → `foHummingbirdMyMerchandiseReturnsPage`
- `addresses/add` → `foHummingbirdAddressesCreatePage`

## Changes

- **Deleted** ~20+ local page object files
- **Updated** ~30+ test files with new imports
- Changed from default exports to named imports
- Updated all page object references in test files

## Test Coverage

Tests affected: audit/BO, audit/FO, functional/BO (dashboard, orders, catalog, customers, customer service)