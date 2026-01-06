# Migrate Functional Tests to `@prestashop-core/ui-testing` (Part 2)

Migrate functional tests to use page objects from the centralized `@prestashop-core/ui-testing` package instead of local implementations. This refactoring removes local page object files and updates test imports to use the shared package.