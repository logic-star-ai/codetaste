# Reorganize network-related packages into `net/` hierarchy

## Summary
Restructure package layout by moving HTTP, RPC, mail, and URL packages under the `net/` directory tree. This is part of the Go 1 package reorganization effort.

## Packages Relocated

Move the following packages:
- `http` → `net/http`
- `http/{cgi,fcgi,pprof,httptest}` → `net/http/{cgi,fcgi,pprof,httptest}`
- `mail` → `net/mail`
- `rpc` → `net/rpc`
- `rpc/jsonrpc` → `net/rpc/jsonrpc`
- `smtp` → `net/smtp`
- `url` → `net/url`

## Changes

- Update Makefile directory lists to reflect new locations
- Adjust relative paths in package Makefiles (`../../Make.inc` → `../../../Make.inc` etc.)
- Update `deps.bash` with sed rules to map old paths to new paths
- Remove `rand` from NOTEST list (now has test coverage)

## Scope

**Source code remains unchanged** - only Makefiles and build configuration affected. Import path updates will be handled separately.