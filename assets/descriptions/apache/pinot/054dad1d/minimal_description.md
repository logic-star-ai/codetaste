# Refactor `StageNode` → `PlanNode` and `stage` → `planFragment` terminology in query planner

Rename all `StageNode` interfaces and implementations to `PlanNode` equivalents, and update query planner terminology from `stage` to `planFragment` to better separate planning and execution concepts.