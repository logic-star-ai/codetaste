#!/usr/bin/env python3
"""
Parse Go test JSON output and produce a summary in the required format.
"""
import json
import sys

def parse_test_output(json_lines):
    """Parse JSON test output and count results."""
    tests = {}
    packages = set()

    for line in json_lines:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        action = event.get('Action')
        package = event.get('Package', '')
        test = event.get('Test', '')

        if action in ('pass', 'fail', 'skip') and test:
            # Track test result
            test_key = f"{package}::{test}"
            tests[test_key] = action
            packages.add(package)
        elif action == 'pass' and not test and package:
            # Package-level pass (all tests in package passed)
            packages.add(package)

    # Count results
    passed = sum(1 for result in tests.values() if result == 'pass')
    failed = sum(1 for result in tests.values() if result == 'fail')
    skipped = sum(1 for result in tests.values() if result == 'skip')
    total = len(tests)

    return {
        'passed': passed,
        'failed': failed,
        'skipped': skipped,
        'total': total
    }

def main():
    """Main function to parse stdin and output JSON summary."""
    json_lines = []
    for line in sys.stdin:
        json_lines.append(line)

    results = parse_test_output(json_lines)
    print(json.dumps(results))

if __name__ == '__main__':
    main()
