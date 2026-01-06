# Refactor flags from underscore to dash notation (Part 4)

Migrate 273 command-line flags from underscore (`_`) to dash (`-`) naming convention across vtbackup, vtcombo, vtctld, vtgate, vttablet, mysqlctl, mysqlctld, and related components. Update all flag definitions, documentation, examples, and tests to use the new dashed format while maintaining backward compatibility.