# Consolidate Bridging Modules: Merge CBasicBridging + CASTBridging into BasicBridging + ASTBridging

Merge `CASTBridging` and `CBasicBridging` modules with their respective parent modules (`ASTBridging` and `BasicBridging`) to enable C++ interop in ASTGen and unify bridging code between ASTGen and SwiftCompilerSources.