# Migrate internal ID handling from raw pointers to IDPtr smart pointers

Refactor internal representation of Zeek identifiers from raw `ID*` pointers to `IDPtr` smart pointers throughout interpreter and script optimization code. Changes `IDPList` from `PList<ID>` to `std::vector<IDPtr>` and `IDSet` from `std::unordered_set<const ID*>` to `std::unordered_set<IDPtr>`.