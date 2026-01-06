# Refactor tctl commands to use lazy auth client initialization

Reorganize tctl command architecture to avoid eagerly initializing auth client connections. Commands now receive a lazy initialization function instead of a pre-connected client, allowing commands that don't need authentication (like `version`) to execute without connecting to the auth server.