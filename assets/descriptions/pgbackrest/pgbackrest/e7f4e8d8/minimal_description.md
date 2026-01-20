# Protocol command multiplexing

Refactor protocol layer to support concurrent file operations on the same remote by introducing sessions and asynchronous request/response multiplexing.