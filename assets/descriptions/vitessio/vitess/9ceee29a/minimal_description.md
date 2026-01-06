# Refactor: Move topo cell map into topo package, introduce Conn interface

Major architectural refactoring of topology server implementation. Moves cell management from individual backend implementations into the central `topo` package. Backends now only provide connection objects (`Conn`) and factory methods instead of managing cells themselves.