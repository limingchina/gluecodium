import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

function assertDefaultStruct(value) {
  assert.equal(value.intField, 42);
  assert.equal(value.uintField, 4294967295);
  assert.ok(Math.abs(value.floatField - 3.14) < 1e-6);
  assert.equal(value.boolField, true);
  assert.equal(value.stringField, "some string");
  assert.equal(value.enumField, module.DefaultsSomeEnum.BAR_VALUE);
}

test("returns C++ default-initialized structs", () => {
  const value = module.Defaults.getDefault();
  assertDefaultStruct(value);
  assert.equal(module.Defaults.checkDefault(value), true);
});

test("returns special numeric defaults", () => {
  const value = module.Defaults.createSpecial();
  assert.ok(Number.isNaN(value.floatNanField));
  assert.equal(value.floatInfinityField, Infinity);
  assert.equal(value.floatNegativeInfinityField, -Infinity);
  assert.ok(Number.isNaN(value.doubleNanField));
  assert.equal(value.doubleInfinityField, Infinity);
  assert.equal(value.doubleNegativeInfinityField, -Infinity);
});

test("returns empty and initializer collection defaults", () => {
  const empty = module.Defaults.getEmptyDefaults();
  assert.deepEqual(empty.intsField, []);
  assert.deepEqual(empty.floatsField, []);
  assert.deepEqual(empty.mapField, new Map());
  assert.deepEqual(empty.setTypeField, new Set());

  const initialized = module.Defaults.getInitializerDefaults();
  assert.deepEqual(initialized.intsField, [4, -2, 42]);
  assert.ok(Math.abs(initialized.floatsField[0] - 3.14) < 1e-6);
  assert.equal(initialized.floatsField[1], -Infinity);
  assert.deepEqual(initialized.setTypeField, new Set(["foo", "bar"]));
  assert.deepEqual(
    initialized.mapField,
    new Map([[1, "foo"], [42, "bar"]]),
  );
});