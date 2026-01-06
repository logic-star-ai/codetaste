# Refactor ConfigData processing to clarify location vs resource concepts

ConfigData processing code uses confusing terminology where "location" refers to both String values and typed instances, making the code awkward to follow with no proper home for `optional:` prefix logic and Origin support.