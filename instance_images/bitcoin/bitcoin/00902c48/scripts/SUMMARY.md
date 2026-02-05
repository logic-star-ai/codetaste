# Summary

Bitcoin Core v0.14 test environment configured successfully for Ubuntu 24.04. The repository is a C++ cryptocurrency node implementation using autotools for building and Python 3 for functional testing.

## System Dependencies

- **Build tools**: build-essential, libtool, autotools-dev, automake, pkg-config
- **Libraries**:
  - libssl-dev (OpenSSL)
  - libevent-dev (event notification)
  - libboost1.74-all-dev (Boost 1.74 - **critical for compatibility**)
  - libdb5.3++-dev (Berkeley DB)
  - libzmq3-dev, python3-zmq (ZeroMQ for notifications)
  - bsdmainutils

**Note**: Ubuntu 24.04 ships with Boost 1.83 by default, which is incompatible with this older Bitcoin Core codebase. Boost 1.74 was explicitly installed to resolve compilation issues.

## Project Environment

The setup applies several compatibility patches to work with modern GCC 13 and Boost 1.74:

1. **httpserver.cpp**: Added `#include <deque>` (missing STL header)
2. **miner.h**: Made `CompareModifiedEntry::operator()` const
3. **txmempool.h**: Made all comparator operators const (4 methods)
4. **lockedpool.cpp**: Added `#include <stdexcept>`
5. **validation.cpp, init.cpp, torcontrol.cpp, validationinterface.cpp**: Added boost::placeholders using declarations

Build configuration:
- Configured with `--with-incompatible-bdb` (uses BDB 5.3 instead of required 4.8)
- Disabled wallet, bench, and Qt components
- Enabled ZMQ for notifications
- Compiled with `-O0 -g` for faster builds

## Testing Framework

The functional tests are Python 3-based integration tests located in:
- HEAD: `test/functional/`
- HEAD~1: `test/rpc-tests/`

Test runner: `test/pull-tester/rpc-tests.py`

The test suite runs:
- blockchain.py
- disablewallet.py
- httpbasics.py
- multi_rpc.py

These tests validate core Bitcoin node functionality including RPC APIs, blockchain operations, and HTTP interface.

## Additional Notes

**Compatibility challenges**:
- The codebase predates C++17 and modern Boost versions
- Boost 1.74 was the latest version that could be made compatible with reasonable patching
- Several C++ standard library includes were missing due to changes in GCC header dependencies
- Boost multi_index comparators needed const qualifiers for Boost 1.74 compatibility
- Boost.Bind placeholders changed behavior and now require explicit namespace qualification

**Test environment**:
- Tests create temporary Bitcoin node instances on random ports
- No system-level Bitcoin daemon installation required
- All tests run in isolation with clean data directories
- Scripts work on both HEAD and HEAD~1 commits despite directory renaming

**Build time**: Full clean build takes approximately 10-15 minutes on 2 cores.
