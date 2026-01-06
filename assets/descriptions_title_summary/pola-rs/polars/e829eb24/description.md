# Remove `polars(_core)::export` module and make dependencies explicit

Remove the `export` module from `polars-core` and `polars` crates. All crates should specify their own dependencies directly instead of accessing them through re-exports.