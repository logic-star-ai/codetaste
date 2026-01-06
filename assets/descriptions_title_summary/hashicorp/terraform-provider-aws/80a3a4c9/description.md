# Remove transparent tagging-only `ModifyPlan` implementations for Plugin Framework resources

Move `SetTagsAll` functionality from explicit resource implementations into framework wrappers, eliminating boilerplate code across ~100 Plugin Framework resources using transparent tagging.