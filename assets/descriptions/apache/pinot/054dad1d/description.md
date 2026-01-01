# Title
Refactor `StageNode` → `PlanNode` and `stage` → `planFragment` terminology in query planner

# Summary
Rename all `StageNode` interfaces and implementations to `PlanNode` equivalents, and update query planner terminology from `stage` to `planFragment` to better separate planning and execution concepts.

# Why
- Separate the concept of `stage` (execution phase) from `planFragment` (planning phase)
- Current naming conflates planning-time structures with runtime execution stages
- Improve clarity by using distinct terminology for distinct phases of query processing

# What Changed

**Interface & Class Renames**:
- `StageNode` → `PlanNode`
- `AbstractStageNode` → `AbstractPlanNode`  
- `StageNodeVisitor` → `PlanNodeVisitor`
- `StageMetadata` → `PlanFragmentMetadata`
- `ExplainPlanStageVisitor` → `ExplainPlanPlanVisitor`

**Package Restructure**:
- `org.apache.pinot.query.planner.stage.*` → `org.apache.pinot.query.planner.plannode.*`

**Methods & Fields**:
- `getStageId()` / `setStageId()` → `getPlanFragmentId()` / `setPlanFragmentId()`
- `_stageId` → `_planFragmentId`
- `isRootStage()` / `isFinalStage()` → `isRootPlanFragment()` / `isFinalPlanFragment()`

**Variables & Parameters**:
- All `stageId` → `planFragmentId`
- All `stageNode` → `planNode`
- All `stageMetadata` → `planFragmentMetadata`

# Scope
- `pinot-query-planner/` module
- `pinot-query-runtime/` module
- All node implementations: `AggregateNode`, `FilterNode`, `JoinNode`, `MailboxReceiveNode`, `MailboxSendNode`, `ProjectNode`, `SetOpNode`, `SortNode`, `TableScanNode`, `ValueNode`, `WindowNode`, `ExchangeNode`
- All visitors and utility classes
- Test files

# Notes
✅ No logical changes - pure refactoring
✅ Maintains backward compatibility at execution layer
✅ Comments and documentation updated throughout