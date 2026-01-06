# Move `stable_mir` back to its own crate

Move `stable_mir` implementation from `rustc_smir` back to the `stable_mir` crate, completing the refactoring to break circular dependencies between crates.