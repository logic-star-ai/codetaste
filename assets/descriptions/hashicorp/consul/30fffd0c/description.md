# Rename gRPC directories from public/private to external/internal

## Summary
Renamed gRPC service directories:
- `agent/grpc/public` → `agent/grpc-external`
- `agent/grpc/private` → `agent/grpc-internal`

Updated all imports, variable names, comments, and documentation accordingly.

## Why
Previous naming conflated two concepts:
- **Port exposure**: dedicated gRPC port vs multiplexed server port
- **API visibility**: suitable for 3rd-party use vs internal-only

New distinction:
- `external/internal` → which port the service uses (dedicated vs multiplexed)
- `public/private` → whether API can be used by 3rd parties (proto definitions)

This separation is necessary because peering replication API needs to be exposed on the dedicated/external port but is not (yet) suitable for 3rd-party consumption.

## Changes
- Renamed directories: `agent/grpc/{public,private}` → `agent/grpc-{external,internal}`
- Updated imports across codebase: `agent/grpc/public/...` → `agent/grpc-external/...`
- Renamed variables: `publicGRPCServer` → `externalGRPCServer`, etc.
- Updated comments referencing public/private gRPC servers
- Updated docs/rpc/README.md with clearer terminology
- Renamed tool: `tools/private-grpc-proxy` → `tools/internal-grpc-proxy`
- Updated proto file paths in generated code