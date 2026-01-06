# Remove transport package abstraction

Remove the `transport` package and its associated abstractions. Replace with direct use of `*http.Client` and a few helper functions. Eliminate the forked `ctxhttp` implementation (`transport/cancellable`) that was maintained solely for mocking purposes.