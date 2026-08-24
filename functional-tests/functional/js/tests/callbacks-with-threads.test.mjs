import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");
const pump = setInterval(() => module.pumpRuntimeQueue(), 0);

test("dispatches a JavaScript interface callback from a native thread", async () => {
  const Listener = module.ThreadedListener.extend("JavaScriptThreadedListener", {
    onEvent(message) {
      this.callback(message);
      return 0n;
    },
    unloaded() {},
  });
  const callback = new Promise((resolve) => {
    const listener = new Listener();
    listener.callback = resolve;

    const notifier = module.ThreadedNotifier.createOnNewThread();
    notifier.notifyOnDetached(listener, "interface callback");
  });

  assert.equal(await callback, "interface callback");
});

test("dispatches a JavaScript lambda callback from a native thread", async () => {
  const callback = new Promise((resolve) => {
    const notifier = module.ThreadedNotifier.createOnNewThread();
    notifier.notifyLambdaOnDetached((message) => resolve(message), "lambda callback");
  });

  assert.equal(await callback, "lambda callback");
});

test.after(() => clearInterval(pump));