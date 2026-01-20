# Add RuleIdentifier to decouple ShardingSphere Rule architecture

Refactor the ShardingSphere rule system from an inheritance-based design to a composition-based approach using the `RuleIdentifier` pattern. This removes the tight coupling between rules and their capabilities by introducing a unified `RuleIdentifiers` container that holds rule-specific identifiers.