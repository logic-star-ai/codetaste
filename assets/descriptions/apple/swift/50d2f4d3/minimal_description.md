# [NFC] Make llvm namespace explicit for Optional and None to prepare for std::optional migration

Phase-1 preparation for migrating from `llvm::Optional` to `std::optional`. Makes the `llvm` namespace explicit for all uses of `Optional` and `None` throughout the Swift compiler codebase.