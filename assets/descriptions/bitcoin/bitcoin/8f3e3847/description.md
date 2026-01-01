Title
-----
Remove `is_network_split` from functional test cases

Summary
-------
Remove `is_network_split` variable from functional test framework and all test cases. This variable forces unnecessary boilerplate in tests and assumptions about network topology.

Why
---
- ~200 LOC of redundant `setup_network()` overrides exist solely to set `is_network_split`
- Variable is only used by 2 test cases but impacts all tests
- Forces assumption of 4-node linear topology (A-B-C-D or split A-B // C-D)
- Makes framework less generic and harder to extend

Changes
-------
**In test_framework.py:**
- Remove `is_network_split` variable
- Update `sync_all()` to accept `node_groups` parameter for flexible network topologies
- Update `split_network()`/`join_network()` to use `disconnect_nodes()`/`connect_nodes()` instead of stop/restart
- Make `setup_network()` more generic with fewer topology assumptions

**In util.py:**
- Add `disconnect_nodes()` helper function
- Add `-uacomment=testnode%d` to node args for peer identification

**In test cases:**
- Remove `self.is_network_split = False` assignments (50+ files)
- Remove custom `setup_network()` methods that only set `is_network_split` (30+ files)
- Move node args from `setup_network()` to `self.extra_args` 
- Call `self.setup_nodes()` instead of manually starting nodes
- Update `sync_all()` calls to pass node_groups where network is split (getchaintips.py, listsinceblock.py)

Benefits
--------
- Removes ~200 lines of unnecessary boilerplate
- 10x speed improvement for tests using split/join (e.g., listsinceblock: 44s → 4.2s)
- More generic framework, easier to support custom topologies
- Cleaner, more maintainable test code