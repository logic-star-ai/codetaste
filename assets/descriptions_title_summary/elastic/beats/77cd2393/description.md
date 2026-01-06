# Replace global logger instances with local logger parameter passing (Part 10)

Continue refactoring code to eliminate direct global logger creation (`logp.NewLogger()`) by accepting logger instances as parameters and using named child loggers instead.