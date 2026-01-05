# Refactor netstack to use bufferv2

## Summary
Replace `pkg/buffer` with `pkg/bufferv2` throughout the netstack implementation. The new buffer implementation uses reference counting and pooling to significantly reduce heap allocations and GC pressure.

## Why
The old buffer implementation caused excessive heap allocations and GC pressure. bufferv2 introduces:
- Reference counting for safer buffer lifecycle management
- Memory pooling to reduce allocations
- Better performance characteristics for network operations

## Performance Impact
Benchmark results (iperf):

**Before:**
- Upload: 1552 ns/op, 46.6GiB allocations
- Download: 1114 ns/op, 68.6GiB allocations

**After:**
- Upload: 1139 ns/op (-27%), 1.41GiB allocations (-97%)
- Download: 753.2 ns/op (-33%), 706MiB allocations (-99%)

## Changes
- Replace `buffer.Buffer` → `bufferv2.Buffer` across netstack
- Replace `buffer.View` → `bufferv2.View` with explicit lifecycle management
- Add `Release()` calls throughout for proper resource cleanup
- Update buffer operations: `AppendOwned()` → `Append()`, `AsBuffer()` → `ToBuffer()`, etc.
- Modified packet handling to use view-based operations instead of byte slices
- Updated all transport/network protocols: TCP, UDP, ICMP, IPv4/IPv6, ARP, ...
- Converted link layer implementations: fdbased, loopback, sniffer, tun, ...
- Added proper cleanup with `defer` for released buffers

## API Changes
Key differences in bufferv2:
- Views are reference counted and must be explicitly released
- Buffers own their views (no more `AppendOwned` vs `Append` distinction)
- `ToView()` and `ToBuffer()` create clones instead of `AsBuffer()` conversions
- Added `WriteFromReader()`, `WriteAt()`, `Grow()`, `CapLength()` for better I/O

## Testing
All existing tests updated and passing with new buffer implementation.