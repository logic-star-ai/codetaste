# Consolidate Golang Plugin Binaries to Reduce Build Time and Package Size

## Summary
Refactor compiled golang plugins to use 3 distinct binaries instead of compiling individual binaries for each subcommand and trigger. Use symlinks to route to appropriate entrypoints.

## Why
- Current approach builds separate binary for each subcommand/trigger → slow compilation
- Many small binaries → larger package size
- Duplicate build overhead across plugins

## Changes

### Build Structure
- **commands**: standalone binary (existing)
- **subcommands/subcommands**: single entrypoint for all subcommands
- **triggers**: single entrypoint for all triggers

### Implementation Pattern
- Replace individual `src/subcommands/*/xyz.go` files → single `src/subcommands/subcommands.go`
- Replace individual `src/triggers/*/xyz.go` files → single `src/triggers/triggers.go`
- Use `strings.Split(os.Args[0], "/")` to determine which subcommand/trigger invoked
- Route to appropriate handler via switch statement
- Move command/trigger logic into main package (`subcommands.go`, `triggers.go` in plugin root)

### Build Process
```makefile
subcommands:
	go build -o subcommands/subcommands src/subcommands/subcommands.go
	$(MAKE) $(SUBCOMMANDS)

subcommands/%:
	ln -sf subcommands $@
```

### Affected Plugins
- buildpacks
- config
- network
- repo  
- resource

## Benefits
- ✅ Faster build process (3 binaries vs. dozens)
- ✅ Smaller package/install size (symlinks vs. copies)
- ✅ Shared build cache across docker builds