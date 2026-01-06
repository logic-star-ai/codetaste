# Flatten `Animated` directory structure by removing legacy `src/` subdirectory

The `Libraries/Animated/` module currently has an unnecessary `src/` subdirectory (`Libraries/Animated/src/`). This refactoring collapses the directory structure by moving all files from `Animated/src/` up one level to `Animated/` and updating all import paths accordingly.