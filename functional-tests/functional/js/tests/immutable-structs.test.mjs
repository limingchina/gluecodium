import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("converts immutable structs through plain JavaScript objects", () => {
  const value = module.Defaults.getImmutableDefault();
  assert.equal(value.intField, 42);
  assert.equal(value.uintField, 0);
  assert.ok(Math.abs(value.floatField - 3.14) < 1e-6);
  assert.equal(value.boolField, false);
  assert.equal(value.stringField, "some string");
  assert.ok(value.enumField !== undefined);
});

test("round-trips nested immutable structs", () => {
  const input = {
    int8Field: -1,
    uint8Field: 255,
    int16Field: -2,
    uint16Field: 65535,
    int32Field: -3,
    uint32Field: 4294967295,
    int64Field: -4n,
    uint64Field: 4n,
    floatField: 1.5,
    doubleField: 2.5,
    stringField: "hello",
    booleanField: true,
    pointField: { x: 7, y: 8 },
  };
  const result = module.PlainDataStructuresImmutable.immutableStructRoundTrip(input);
  assert.deepEqual(result, input);

  const nested = module.PlainDataStructuresImmutable.nestingImmutableStructRoundTrip({
    structField: input,
  });
  assert.deepEqual(nested.structField, input);
});