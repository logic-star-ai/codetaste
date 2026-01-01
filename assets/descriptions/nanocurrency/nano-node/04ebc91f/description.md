Title
-----
Refactor store iterators from polymorphism to std::variant

Summary
-------
Convert database store iterators from inheritance-based polymorphic design to variant-based implementation using `std::variant<lmdb::iterator, rocksdb::iterator>`.

Why
---
- **Eliminate heap allocations**: Polymorphic iterators required heap allocation via `std::unique_ptr`; variants are stack-allocated
- **Simplify iterator construction**: Remove complex inheritance hierarchy and virtual function overhead
- **Enable complex iterator patterns**: Variant-based design allows more flexible iterator compositions that were difficult with polymorphism
- **Improve performance**: Stack allocation + no virtual dispatch = faster iteration in performance-critical paths

Changes
-------
**Iterator Architecture (3 layers)**:
- **Base database iterators**: `lmdb::iterator` / `rocksdb::iterator` using native types (`MDB_val` / `Slice`)
- **Generic iterator**: `store::iterator` holding variant, adapts native types to `std::span<uint8_t>`
- **Typed iterator**: `store::typed_iterator<Key, Value>` providing strong typing for key/value pairs

**Iterator Semantics**:
- Bi-directional with sentinel value for end
- Circular: `++end()` → first element, `--end()` → last element
- No more null iterator comparisons

**Reverse Iteration**:
- Replace `rbegin()` returning reverse-positioned forward iterator
- Add proper `reverse_iterator` adapter inverting increment/decrement semantics
- `rend()` now returns reverse iterator sentinel (not `end()`)

**Implementation Details**:
- Remove `iterator_impl<T,U>` base class + virtual functions
- Remove heap-allocated `std::unique_ptr<iterator_impl>` wrappers
- Add `typed_iterator_templ.hpp` / `reverse_iterator_templ.hpp` for generic implementations
- Update LMDB/RocksDB iterators as standalone classes with factory methods (`begin()`, `end()`, `lower_bound()`)
- Change iterator construction: `iterator{nullptr}` → `iterator{lmdb::iterator::end(...)}`

**Breaking Changes**:
- Iterator comparison now checks internal variant equality (not pointer equality)
- Reverse iteration: `--i` in forward loops → `++i` in reverse loops (adaptor inverts semantics)
- Constructor signatures changed across all store implementations

**Files Modified**:
- Removed: `iterator_impl.{hpp,cpp}`
- Added: `typed_iterator.{hpp,cpp,_templ.hpp}`, `reverse_iterator.{hpp,_templ.hpp}`, `rocksdb/utility.{hpp,cpp}`
- Updated: All store implementations (LMDB/RocksDB account, block, confirmation_height, final_vote, online_weight, peer, pending, pruned, rep_weight)