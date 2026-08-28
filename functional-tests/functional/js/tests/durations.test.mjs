import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("round-trips second durations as bigint ticks", () => {
  assert.equal(module.DurationSeconds.increaseDuration(42n), 43n);
  assert.equal(module.DurationSeconds.increaseDuration(42042n), 42043n);
  assert.equal(module.DurationSeconds.increaseDurationMaybe(42n), 43n);
  assert.equal(module.DurationSeconds.increaseDurationMaybe(null), undefined);
});

test("round-trips millisecond durations without losing sub-second values", () => {
  assert.equal(module.DurationMilliseconds.increaseDuration(42042n), 43042n);
  assert.equal(module.DurationMilliseconds.increaseDurationMaybe(42042n), 43042n);
  assert.equal(module.DurationMilliseconds.increaseDurationMaybe(null), undefined);
});

test("round-trips duration value objects", () => {
  const seconds = module.DurationSeconds.durationStructRoundTrip({ durationField: 42n });
  const milliseconds = module.DurationMilliseconds.durationStructRoundTrip({ durationField: 42042n });

  assert.equal(seconds.durationField, 42n);
  assert.equal(milliseconds.durationField, 42042n);
});

test("selects the duration overload", () => {
  assert.equal(module.DurationOverloads.durationFunction(42n), "duration overload");
  assert.equal(module.DurationOverloads.durationFunction("42"), "string overload");
});