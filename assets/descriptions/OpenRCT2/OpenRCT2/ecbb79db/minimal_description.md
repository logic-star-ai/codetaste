# Adopt existing namespaces into OpenRCT2 namespace hierarchy

Restructure existing namespaces to nest under `OpenRCT2::` root namespace. Add temporary `using namespace OpenRCT2` statements to compilation units to maintain compilation during this transitional refactoring phase.