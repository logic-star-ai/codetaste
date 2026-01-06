# Remove commons-logging dependency and migrate to SLF4J

Remove all references to Apache Commons Logging and migrate to SLF4J-based logging throughout the Hadoop codebase. Restrict future usage through Maven Enforcer rules.