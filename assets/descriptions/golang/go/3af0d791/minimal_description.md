# Delay variable declarations and eliminate dead code in cmd/*g compilers

Refactor compiler code to move variable declarations as close to their point of use as possible, split disjoint uses of variables into separate declarations, and remove unreachable dead code.