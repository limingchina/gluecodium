import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("exports scalar, enum, and special numeric constants", () => {
  assert.equal(module.Constants.INT_CONSTANT, -11);
  assert.equal(module.Constants.UINT_CONSTANT, 4294967295);
  assert.ok(Math.abs(module.Constants.FLOAT_CONSTANT - 2.71) < 1e-6);
  assert.equal(module.Constants.STRING_CONSTANT, "Foo bar");
  assert.equal(module.Constants.ENUM_CONSTANT, module.ConstantsStateEnum.ON);
  assert.ok(Number.isNaN(module.Constants.FLOAT_NAN));
  assert.equal(module.Constants.DOUBLE_INFINITY, Infinity);
  assert.equal(module.Constants.FLOAT_NEGATIVE_INFINITY, -Infinity);
});

test("exports constants declared on classes", () => {
  assert.equal(module.ConstantsInterface.INT_CONSTANT, -11);
  assert.equal(module.ConstantsInterface.UINT_CONSTANT, 42);
  assert.equal(module.ConstantsInterface.STRING_CONSTANT, "Foo bar");
  assert.equal(
    module.ConstantsInterface.ENUM_CONSTANT,
    module.ConstantsInterfaceStateEnum.ON,
  );
});

test("exports struct constants", () => {
  assert.equal(module.StructConstants.STRUCT_CONSTANT.stringField, "bar Buzz");
  assert.ok(Math.abs(module.StructConstants.STRUCT_CONSTANT.floatField - 1.41) < 1e-6);
  assert.equal(
    module.StructConstants.NESTING_STRUCT_CONSTANT.structField.stringField,
    "nonsense",
  );
});

test("omits constants skipped from C++", () => {
  assert.equal(module.ConstantsSkipCpp.BOOL_CONSTANT, undefined);
  assert.equal(module.ConstantsSkipCpp.INT_CONSTANT, undefined);
});