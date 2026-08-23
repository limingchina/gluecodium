// Headless Chromium pass for the pthreads callbacks spike. Requires Playwright:
//
//   npm install playwright && npx playwright install chromium
//
// Start the COOP/COEP server first (node serve.mjs), then run this script.
// The probe is expected to reproduce the "val accessed from wrong thread"
// abort observed in Node.js, now under real cross-origin isolation.
import { chromium } from "playwright";

const url = process.argv[2] ?? "http://localhost:8080/test.html";
const timeoutMs = 30000;

const browser = await chromium.launch();
try {
    const page = await browser.newPage();
    page.on("console", (message) => console.log(`[page] ${message.text()}`));
    page.on("pageerror", (error) => console.log(`[pageerror] ${error.message}`));

    await page.goto(url);
    await page.waitForFunction(() => document.title === "done", null, { timeout: timeoutMs });

    const result = await page.evaluate(() => window.__spikeResult);
    const text = result.join("\n");
    console.log(text);

    if (!/crossOriginIsolated is false/.test(text) === false) {
        console.error("FAIL: page is not cross-origin isolated; SharedArrayBuffer unavailable");
        process.exit(1);
    }
    if (!/wrong thread/i.test(text)) {
        console.error("FAIL: expected 'val accessed from wrong thread' abort");
        process.exit(1);
    }
    console.log("PASS: thread-affinity assertion reproduced in browser under COOP/COEP");
} finally {
    await browser.close();
}
