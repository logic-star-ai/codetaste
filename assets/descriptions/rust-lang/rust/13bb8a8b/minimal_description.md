# Rename `hir::Map::{get_,find_}parent_node` methods and add convenience helpers

Rename `hir::Map::get_parent_node` → `parent_id` and `find_parent_node` → `opt_parent_id`. Add new `get_parent` and `find_parent` methods that return `Node` directly.