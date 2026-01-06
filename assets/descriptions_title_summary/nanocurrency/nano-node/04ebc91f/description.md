# Refactor store iterators from polymorphism to std::variant

Convert database store iterators from inheritance-based polymorphic design to variant-based implementation using `std::variant<lmdb::iterator, rocksdb::iterator>`.