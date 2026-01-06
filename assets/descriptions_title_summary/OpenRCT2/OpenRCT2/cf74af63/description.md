# Reduce Scenario.h Header Dependencies and Remove Unnecessary Includes

Remove `Scenario.h` include from ~50 compilation units that don't actually need it, and slim down the `Scenario.h` header itself by removing unnecessary transitive dependencies.