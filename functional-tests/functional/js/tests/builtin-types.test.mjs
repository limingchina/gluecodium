import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("boolean methods map to JavaScript booleans", () => {
  const methods = module.StaticBooleanMethods;

  assert.equal(methods.returnInvertedBoolean(true), false);
  assert.equal(methods.returnInvertedBoolean(false), true);
  assert.equal(methods.returnAndBoolean(true, true), true);
  assert.equal(methods.returnAndBoolean(true, false), false);
});

test("float and double methods map to JavaScript numbers", () => {
  const methods = module.StaticFloatDoubleMethods;

  assert.equal(methods.returnFloat(1.5), 1.5);
  assert.equal(methods.returnIncrementedFloat(1.5), 2.5);
  assert.equal(methods.sumTwoFloats(1.5, 2.5), 4.0);
  assert.equal(methods.returnDouble(1.5), 1.5);
  assert.equal(methods.returnIncrementedDouble(1.5), 2.5);
  assert.equal(methods.sumTwoDoubles(1.5, 2.5), 4.0);
});

test("integer methods preserve values through embind", () => {
  const methods = module.StaticIntMethods;

  assert.equal(methods.returnNextNumberInt8(1), 2);
  assert.equal(methods.sumTwoNumbersInt8(1, 2), 3);
  assert.equal(methods.returnPrimeInt8(), 2);
  assert.equal(methods.returnNextNumberUint8(1), 2);
  assert.equal(methods.returnPrimeUint8(), 131);
  assert.equal(methods.returnNextNumberInt16(1), 2);
  assert.equal(methods.returnPrimeInt16(), 257);
  assert.equal(methods.returnNextNumberUint16(1), 2);
  assert.equal(methods.returnPrimeUint16(), 32771);
  assert.equal(methods.returnNextNumberInt32(1), 2);
  assert.equal(methods.returnPrimeInt32(), 65537);
  assert.equal(methods.returnNextNumberUint32(1), 2);
  assert.equal(methods.returnPrimeUint32(), 2147483659);
  assert.equal(methods.returnNextNumberInt64(1n), 2n);
  assert.equal(methods.returnPrimeInt64(), 4294967311n);
  assert.equal(methods.returnNextNumberUint64(1n), 2n);
  assert.equal(methods.returnPrimeUint64(), 4294967311n);
});