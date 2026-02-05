#!/bin/bash
# Wrapper to ensure tests run in the correct environment
set -e

# Source the setup in the current shell
source /scripts/setup_shell.sh >/dev/null 2>&1

# Now run a simpler test command directly
cd /testbed
TMP=$(mktemp -d /tmp/juju-test-XXX)
trap "rm -rf $TMP" EXIT

# Get test packages
PKGS=$(go list -f '{{if .TestGoFiles}}{{.ImportPath}}{{end}}' ./... | grep -v '/vendor/' | grep -v '/mocks' | grep -v '/generate/' | grep -E '(github.com/juju/juju/api$|github.com/juju/juju/api/|github.com/juju/juju/jujuclient|github.com/juju/juju/rpc)' | head -15)

# Run tests and capture output
go test -v -count=1 -mod=readonly -tags="${TEST_BUILD_TAGS}" -timeout=600s -check.v $PKGS > $TMP/out.txt 2>&1

# Parse results
cat $TMP/out.txt

PASSED=$(grep -c "^OK: .* passed" $TMP/out.txt | awk '{s+=$1} END {print s+0}' || echo 0)
if [ "$PASSED" -eq 0 ]; then
    PASSED=$(grep -c "^ok  " $TMP/out.txt || echo 0)
fi
FAILED=$(grep "^FAIL" $TMP/out.txt | grep -c "github.com/juju/juju" || echo 0)
SKIPPED=$(grep -c "^--- SKIP:" $TMP/out.txt || echo 0)
TOTAL=$((PASSED + FAILED + SKIPPED))

echo "{\"passed\": $PASSED, \"failed\": $FAILED, \"skipped\": $SKIPPED, \"total\": $TOTAL}"
