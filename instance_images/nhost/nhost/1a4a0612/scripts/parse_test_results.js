#!/usr/bin/env node
// Parse vitest JSON test results from turbo output

const fs = require('fs');

// Read the test output
const output = fs.readFileSync('/tmp/test_output.txt', 'utf8');

let totalPassed = 0;
let totalFailed = 0;
let totalSkipped = 0;
let totalTests = 0;

// The output contains test results for multiple packages
// Each package has a JSON with summary fields like numPassedTests, numFailedTests, etc.
// We look for these fields directly in lines with the :test: prefix
const lines = output.split('\n');

for (const line of lines) {
    // Look for lines containing test summary fields with the turbo prefix
    if (line.includes(':test:') && line.includes('"numTotalTests":')) {
        const match = line.match(/"numTotalTests":\s*(\d+)/);
        if (match) {
            totalTests += parseInt(match[1]);
        }
    }
    if (line.includes(':test:') && line.includes('"numPassedTests":')) {
        const match = line.match(/"numPassedTests":\s*(\d+)/);
        if (match) {
            totalPassed += parseInt(match[1]);
        }
    }
    if (line.includes(':test:') && line.includes('"numFailedTests":')) {
        const match = line.match(/"numFailedTests":\s*(\d+)/);
        if (match) {
            totalFailed += parseInt(match[1]);
        }
    }
    if (line.includes(':test:') && line.includes('"numPendingTests":')) {
        const match = line.match(/"numPendingTests":\s*(\d+)/);
        if (match) {
            totalSkipped += parseInt(match[1]);
        }
    }
}

console.log(JSON.stringify({
    passed: totalPassed,
    failed: totalFailed,
    skipped: totalSkipped,
    total: totalTests
}));
