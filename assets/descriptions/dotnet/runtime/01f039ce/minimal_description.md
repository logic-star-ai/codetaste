# Remove remaining CRT PAL wrappers and enable standard headers in CoreCLR build

Refactor CoreCLR to use standard C/C++ library headers and functions instead of Platform Abstraction Layer (PAL) wrappers, eliminating custom implementations and simplifying the build system.