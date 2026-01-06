# Remove evm/config/v2 versioning; reorganize into config and config/toml packages

Refactor `core/chains/evm/config` package structure to eliminate v2 versioning and improve organization by splitting into interface/implementation (`config`) and TOML type definitions (`config/toml`) packages.