# Title
Migrate Functional Tests to `@prestashop-core/ui-testing` (Part 3)

# Summary
Continue migration of functional tests from local page objects to `@prestashop-core/ui-testing` library. Replace remaining BO/FO page object imports with centralized versions.

# Scope
- **BO Catalog**: Categories, Attributes, Features, Files, Stocks/Movements, Catalog Price Rules
- **BO International**: Taxes, Tax Rules
- **FO Pages**: Sitemap (Classic & Hummingbird)
- **Test Files**: ~30 test files across audit, functional, and monitoring suites

# Changes
- Replace local page imports → `@prestashop-core/ui-testing` imports
- Update naming convention:
  - `categoriesPage` → `boCategoriesPage`
  - `addCategoryPage` → `boCategoriesCreatePage`
  - `featuresPage` → `boFeaturesPage`
  - `viewFeaturePage` → `boFeaturesViewPage`
  - `filesPage` → `boFilesPage`
  - `movementsPage` → `boStockMovementsPage`
  - `taxesPage` → `boTaxesPage`
  - `taxRulesPage` → `boTaxRulesPage`
  - `siteMapPage` → `foClassicSitemapPage` / `foHummingbirdSitemapPage`
  - ... (similar pattern for all migrated pages)
- Delete obsolete page object files:
  - `tests/UI/pages/BO/catalog/categories/...`
  - `tests/UI/pages/BO/catalog/features/...`
  - `tests/UI/pages/BO/catalog/files/...`
  - `tests/UI/pages/BO/catalog/stocks/movements/...`
  - `tests/UI/pages/BO/international/taxes/...`
  - `tests/UI/pages/FO/.../siteMap/...`

# Benefits
- Centralized page object maintenance
- Consistency across test suites
- Reduced code duplication
- Easier updates & maintenance

# Technical Details
- No BC breaks
- No functional changes
- Pure refactoring (import paths + method calls)
- All tests remain functionally identical