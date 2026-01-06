# Remove six dependency from awscli codebase

Remove all usage of the `six` library throughout the AWS CLI v1 codebase now that Python 2 support has been dropped. Replace `six` compatibility utilities with their native Python 3 equivalents.