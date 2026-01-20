# Refactor Authentication SPI and Picketlink to use ProviderSession

Refactor provider lifecycle management to support proper dependency injection and component dependencies. Remove `KeycloakRegistry` in favor of `ProviderSession`-based dependency resolution.