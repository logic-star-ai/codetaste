# Add custom MongoDB interface for entity collections

Introduce custom `MongoCollection` interface to wrap MongoDB driver's `MongoCollection` for entities implementing `MongoEntity`. This provides better control over data modification operations and enforces type constraints at the API level.