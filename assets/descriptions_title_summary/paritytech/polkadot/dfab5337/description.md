# Refactor PVF workers into separate crates with inverted dependencies

Split the monolithic `polkadot-node-core-pvf-worker` crate into three focused crates: `pvf-common`, `pvf-execute-worker`, and `pvf-prepare-worker`. Invert the dependency relationship so workers no longer depend on the host crate.