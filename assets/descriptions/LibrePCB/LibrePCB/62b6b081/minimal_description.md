# Remove QtWidgets dependency from CLI and core library

Refactor the `Application` class to eliminate QtWidgets dependency from the CLI binary and core library. Convert `Application` from a `QApplication` subclass to a static utility class, enabling the CLI to run with `QGuiApplication` instead.