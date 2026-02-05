// Custom Playwright config for test script
// Based on tests/playwright.config.ts but without webServer
import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 40000,
  fullyParallel: true,
  snapshotDir: '/testbed/tests/snapshots',
  snapshotPathTemplate: '/testbed/tests/snapshots/{testFilePath}/{arg}{ext}',
  testDir: '/testbed/tests',
  use: {
    browserName: 'chromium',
    viewport: { width: 960, height: 900 },
    trace: 'on-first-retry',
    video: 'on-first-retry',
    actionTimeout: 5_000,
    permissions: ['clipboard-read', 'clipboard-write'],
    baseURL: 'http://localhost:5173',
  },
  workers: 4, // Reduced to avoid resource exhaustion
  retries: 0,
  reporter: 'list',
});
