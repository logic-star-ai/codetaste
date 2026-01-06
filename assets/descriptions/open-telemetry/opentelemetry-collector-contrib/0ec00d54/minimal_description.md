# Remove BuildContext Abstraction

Remove the `BuildContext` struct that was used to pass configuration during operator building. Replace with direct `*zap.SugaredLogger` parameter in `Build()` methods.