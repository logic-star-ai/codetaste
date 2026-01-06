# Refactor: Extract in-process test HTTP servers into separate processes

Refactor test infrastructure to run HTTP/HTTPS mock servers as separate subprocesses instead of in-process `reactor.listen*` instances, improving test isolation and reliability.