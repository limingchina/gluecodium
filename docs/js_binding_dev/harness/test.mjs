import assert from "node:assert/strict";
import createModule from "./phase4_harness.mjs";

const Module = await createModule();
const Harness = Module.Harness;

assert.equal(typeof Harness.add, "function");
assert.equal(Harness.add(20, 22), 42);

console.log("Phase 4 harness OK");
