# Remove `LetRec` expression node from AST

## Summary
Remove the `LetRec` expression node from all compiler AST representations and replace its functionality with `LocalDef`.

## Why
- Simplifies the AST by consolidating recursive let bindings with local definitions
- Reduces redundancy in expression handling across compiler phases
- `LocalDef` already handles recursive function definitions adequately

## Changes

**AST Nodes**
- Remove `LetRec` case classes from:
  - `DesugaredAst`, `WeededAst`, `NamedAst`, `ResolvedAst`, `KindedAst`, `TypedAst`
  - `LoweredAst`, `MonoAst`, `SimplifiedAst`, `LiftedAst`, `ReducedAst`, `OccurrenceAst`

**Pattern Matching**
- Remove `LetRec` cases from:
  - LSP providers (`Indexer`, `SemanticTokensProvider`)
  - AST printers (all printer phases)
  - Compiler phases: `ClosureConv`, `Desugar`, `EffectBinder`, `EffectVerifier`, `Eraser`, `Inliner`, `Kinder`, `LambdaLift`, `Lowering`, `Monomorpher`, `Namer`, `OccurrenceAnalyzer`, `PatMatch`, `PredDeps`, `Reducer`, `Redundancy`, `Regions`, `Resolver`, `Safety`, `Simplifier`, `Stratifier`, `TailPos`, `TreeShaker1`, `TreeShaker2`, `TypeReconstruction`, `VarOffsets`, `Verifier`, `ConstraintGen`, etc.

**Parser**
- Rename `TreeKind.Expr.LetRecDef` → `TreeKind.Expr.LocalDef`
- Update `letRecDefExpr()` → `localDefExpr()`
- Update comments referencing `LetRecDef` → `LocalDef`

**Bytecode Generation**
- Remove special handling for recursive closures in `GenExpression`