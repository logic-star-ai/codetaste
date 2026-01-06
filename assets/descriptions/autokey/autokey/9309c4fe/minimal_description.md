# Split model module into separate files and resolve circular imports

Refactor `autokey.model.__init__.py` by splitting it into separate modules for each class, and move `Key` class + constants from `iomediator` to `model` package to break circular dependencies.