# Refactor tctl commands to support lazy auth client initialization

Reorganize tctl command structure to enable commands that don't require authentication (e.g., `version`) to run without establishing an auth server connection.