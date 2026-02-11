#!/usr/bin/env python3
"""Parse Go test JSON output and count results."""

import json
import sys

passed = 0
failed = 0
skipped = 0

for line in sys.stdin:
    try:
        data = json.loads(line.strip())
        action = data.get('Action', '')
        test = data.get('Test', '')

        # Only count top-level tests (no slashes in test name)
        # Skip empty test names (package-level results)
        if test and '/' not in test:
            if action == 'pass':
                passed += 1
            elif action == 'fail':
                failed += 1
            elif action == 'skip':
                skipped += 1
    except (json.JSONDecodeError, ValueError):
        # Skip non-JSON lines
        continue

total = passed + failed + skipped
print(json.dumps({
    "passed": passed,
    "failed": failed,
    "skipped": skipped,
    "total": total
}))
