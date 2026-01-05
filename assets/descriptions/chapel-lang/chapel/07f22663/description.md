# Title
Rename `Attributes` to `AttributeGroup` and move to `AstNode` base class

## Summary
Rename uast node `Attributes` → `AttributeGroup` and move attribute storage from `Decl` to `AstNode` base class. Replace all literal `-1` "no-child" indicators with `AstNode::NO_CHILD` constant.

## Why
Enable placing attributes on loops and other non-decl AST nodes by providing attribute support at the base `AstNode` level rather than restricting it to `Decl` subclasses.

## Changes
- Rename `Attributes` class → `AttributeGroup`
- Move `attributeGroupChildNum_` field from `Decl` to `AstNode`
- Rename methods: `attributes()` → `attributeGroup()`, `idToAttributes()` → `idToAttributeGroup()`
- Rename parser context: `AttributeParts` → `AttributeGroupParts`, `hasAttributeParts` → `hasAttributeGroupParts`, etc.
- Replace all `-1` literals with `AstNode::NO_CHILD` constant throughout uast constructors
- Update `AstNode` constructors to accept `attributeGroupChildNum` parameter
- Update all `build()` methods to use `owned<AttributeGroup>` instead of `owned<Attributes>`
- Update serialization/deserialization to handle new field location
- Update `convert-uast.cpp`, `chpldoc.cpp`, and all tests

## Files affected
- `frontend/include/chpl/uast/{Attributes.h → AttributeGroup.h}`
- `frontend/lib/uast/{Attributes.cpp → AttributeGroup.cpp}`
- `frontend/include/chpl/uast/{AstNode,Decl,*}.h`
- `frontend/lib/uast/*.cpp`
- `frontend/lib/parsing/{ParserContext,parsing-queries,bison-chpl-lib}.*`
- `compiler/passes/convert-uast.cpp`
- `tools/chpldoc/chpldoc.cpp`
- All test files