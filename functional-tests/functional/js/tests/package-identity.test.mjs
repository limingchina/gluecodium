import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const testPackage = await loadPackage("test");
const underscorePackage = await loadPackage("test_off");
const fooPackage = await loadPackage("test/foo");
const barPackage = await loadPackage("test/bar");

test("keeps underscore-prefixed package paths available", () => {
  assert.equal(typeof underscorePackage.OffInterface, "function");
  assert.equal(typeof underscorePackage.OffStruct, "object");
  assert.equal(typeof testPackage.UseUnderscorePackage, "function");

  assert.deepEqual(
    testPackage.UseUnderscorePackage.methodWithUnderscoreStruct({ structField: "value" }),
    { structField: "" },
  );
});

test("keeps equal public leaf names distinct across packages", () => {
  assert.notEqual(testPackage.Alphabet, fooPackage.Alphabet);
  assert.notEqual(testPackage.Alphabet, barPackage.Alphabet);
  assert.equal(typeof testPackage.Alphabet.A, "object");
  assert.equal(typeof fooPackage.Alphabet.BETA, "object");
  assert.equal(typeof barPackage.Alphabet.GIMEL, "object");
});