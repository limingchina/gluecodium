import assert from "node:assert/strict";
import createModule from "./phase4_harness.mjs";

const Module = await createModule();
const Harness = Module.Harness;
const Mode = Module.Mode;
const MultipleInheritanceFactory = Module.MultipleInheritanceFactory;

assert.equal(typeof Harness.add, "function");
assert.equal(Harness.add(20, 22), 42);

const harness = Harness.create(10);
assert.equal(harness.value, 10);
assert.equal(harness.increment(5), 15);
assert.equal(harness.value, 15);
assert.equal(harness.nullableValue(7), 7);
assert.equal(harness.nullableValue(null), undefined);
assert.equal(harness.sum([1, 2, 3, 4]), 10);
assert.equal(harness.lookup(new Map([["answer", 42]]), "answer"), 42);
assert.equal(harness.lookup(new Map(), "missing"), undefined);

const sample = { count: 3, label: "three" };
const copiedSample = harness.roundTrip(sample);
assert.equal(copiedSample.count, 3);
assert.equal(copiedSample.label, "three");
assert.equal(harness.roundTripMode(Mode.ON), Mode.ON);
assert.equal(harness.roundTripLong(9007199254740993n), 9007199254740993n);

harness.delete();

const multi = MultipleInheritanceFactory.getMultiClass();
assert.equal(typeof multi.parentFunction, "function");
assert.equal(multi.parentProperty, "open-parent");
assert.equal(multi.parentFunctionLight(), "narrow-parent");
assert.equal(multi.parentPropertyLight, "narrow-property");
assert.equal(multi.childFunction(), "child");
assert.equal(multi.childProperty, "child-property");

const narrow = MultipleInheritanceFactory.upcastToNarrow(multi);
assert.equal(narrow.parentFunctionLight(), "narrow-parent");
assert.equal(narrow.parentPropertyLight, "narrow-property");

const separateNarrow = MultipleInheritanceFactory.getMultiClassAsNarrow();
assert.notEqual(narrow, separateNarrow);

multi.delete();
narrow.delete();
separateNarrow.delete();

console.log("Phase 5 harness OK");
