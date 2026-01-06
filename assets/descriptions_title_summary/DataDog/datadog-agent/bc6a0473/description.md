# Move provisioners to dedicated package to avoid circular dependencies

Extract all provisioner-related code from `pkg/e2e` and `pkg/environments` into a new dedicated `pkg/provisioners` package to enable cleaner separation of concerns and avoid circular dependencies.