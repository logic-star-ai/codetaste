Title
-----
Fix includes and build files after source reorganization

Summary
-------
Update all `#include` statements and CMake build configuration to reflect new source directory structure after files were moved into subdirectories.

Changes
-------
- Updated `src/CMakeLists.txt` to reference files in new locations:
  - `lua/` ... Lua integration, settings, config
  - `content/` ... colours, gradients, specials, templates, text objects
  - `data/` ... data collection subsystems
    - `data/audio/` ... mixer, mpd, audacious, cmus, pulseaudio, etc.
    - `data/hardware/` ... cpu, diskio, i8k, ibm, nvidia, intel_backlight, etc.
    - `data/network/` ... mail, net_stat, rss, irc, ccurl_thread, etc.
    - `data/os/` ... linux, freebsd, darwin, openbsd, netbsd, etc.
  - `output/` ... display backends (X11, Wayland, ncurses, console, file, http)
- Fixed all `#include` paths throughout codebase (*.cc, *.h, *.hh, *.mm files)
- Adjusted relative include paths (e.g., `"conky.h"` → `"../conky.h"`, `"logging.h"` → `"../../logging.h"`)
- Updated test files in `tests/` directory to use new paths

Why
---
Part 2 of source reorganization (part 1 moved files, this commit fixes references). Build system and all source files need to reference correct paths for compilation to succeed.