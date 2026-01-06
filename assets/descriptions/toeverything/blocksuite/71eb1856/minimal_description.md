# Refactor database table view to decouple rendering from model

Decouple database table rendering from the model layer by introducing a `TableViewManager` abstraction. This allows any data source implementing the interface to be rendered as a table, improving modularity and separation of concerns.