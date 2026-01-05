# Title

Migrate Functional Tests to `@prestashop-core/ui-testing` (Part 4)

# Summary

Refactor functional tests to use centralized page objects from `@prestashop-core/ui-testing` package. This batch covers BO Catalog (brands, suppliers, files), Customer Service, Customers Outstanding, Design Pages, International Zones, Modules, and FO Classic/Hummingbird pages.

# Why

- Consolidate page objects into single testing library
- Enforce consistent naming conventions across test files
- Reduce code duplication
- Improve maintainability of test suite
- Standardize page object patterns

# Changes

**Import Migration:**
- Remove local page object imports (`@pages/BO/...`, `@pages/FO/...`)
- Replace with centralized imports from `@prestashop-core/ui-testing`

**Naming Standardization:**
```
addBrandPage → boBrandsCreatePage
addBrandAddressPage → boBrandAdressesCreatePage
viewBrandPage → boBrandsViewPage
suppliersPage → boSuppliersPage
viewSupplierPage → boSuppliersViewPage
boSuppliersCreate → boSuppliersCreatePage
addFilePage → boFilesCreatePage
addOrderMessagePage → boOrderMessagesCreatePage
outstandingPage → boOutstandingPage
viewPage → boCustomerServiceViewPage
pagesPage → boCMSPagesPage
addPageCategoryPage → boCMSPageCategoriesCreatePage
zonesPage → boZonesPages
moduleConfigurationPage → boModuleConfigurationPage
blockCartModal → foClassicModalBlockCartPage
createAccountPage → foClassicCreateAccountPage
addressesPage → foClassicMyAddressesPage
addAddressPage → foClassicMyAddressesCreatePage
vouchersPage → foClassicMyVouchersPage
```

**Files Affected:**
- Audit tests (BO catalog, customer service, design, international, FO guest/connected)
- Functional tests (brands, suppliers, files, cart rules, customers, customer service, outstanding, design pages, zones, modules)
- FO Classic: modal, myAccount pages (add, addAddress, addresses, vouchers)
- FO Hummingbird: modal, myAccount pages

**Deleted Page Objects:**
- `tests/UI/pages/BO/catalog/brands/...`
- `tests/UI/pages/BO/catalog/suppliers/...`
- `tests/UI/pages/BO/catalog/files/...`
- `tests/UI/pages/BO/customerService/...`
- `tests/UI/pages/BO/customers/outstanding/...`
- `tests/UI/pages/BO/design/pages/...`
- `tests/UI/pages/BO/international/locations/...`
- `tests/UI/pages/BO/modules/...`
- `tests/UI/pages/FO/classic/modal/blockCart.ts`
- `tests/UI/pages/FO/classic/myAccount/...`
- `tests/UI/pages/FO/hummingbird/modal/blockCart.ts`
- `tests/UI/pages/FO/hummingbird/myAccount/...`

# Scope

Part 4 focuses on:
- BO: Catalog (brands/suppliers/files) • Customer Service • Customers Outstanding • Design Pages • International Zones • Modules
- FO: Classic & Hummingbird (modals, account pages)