#!/usr/bin/env python3
"""Parse PHPUnit JUnit XML output and return JSON summary"""
import json
import sys
import xml.etree.ElementTree as ET


def parse_phpunit_xml(xml_file):
    """Parse PHPUnit JUnit XML file and extract test statistics"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # The root testsuites element contains the summary
        if root.tag == 'testsuites':
            # Get the first testsuite which has the aggregate stats
            testsuite = root.find('testsuite')
            if testsuite is not None:
                tests = int(testsuite.get('tests', 0))
                failures = int(testsuite.get('failures', 0))
                errors = int(testsuite.get('errors', 0))
                skipped = int(testsuite.get('skipped', 0))

                passed = tests - failures - errors - skipped

                return {
                    'passed': passed,
                    'failed': failures + errors,
                    'skipped': skipped,
                    'total': tests
                }

        # Fallback if structure is different
        return {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }
    except Exception as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        return {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: parse_phpunit_xml.py <xml_file>", file=sys.stderr)
        sys.exit(1)

    result = parse_phpunit_xml(sys.argv[1])
    print(json.dumps(result))
