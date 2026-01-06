# Rename `Attributes` to `AttributeGroup` and move to `AstNode` base class

Rename uast node `Attributes` → `AttributeGroup` and move attribute storage from `Decl` to `AstNode` base class. Replace all literal `-1` "no-child" indicators with `AstNode::NO_CHILD` constant.