// Custom Playwright reporter that outputs JSON summary
class JsonReporter {
  constructor() {
    this.stats = {
      passed: 0,
      failed: 0,
      skipped: 0,
      total: 0
    };
  }

  onBegin(config, suite) {
    this.stats.total = suite.allTests().length;
  }

  onTestEnd(test, result) {
    if (result.status === 'passed' || result.status === 'expected') {
      this.stats.passed++;
    } else if (result.status === 'failed' || result.status === 'timedOut' || result.status === 'unexpected') {
      this.stats.failed++;
    } else if (result.status === 'skipped' || result.status === 'interrupted') {
      this.stats.skipped++;
    }
  }

  onEnd(result) {
    // Output JSON to stdout as the last line
    console.log(JSON.stringify(this.stats));
  }
}

export default JsonReporter;
