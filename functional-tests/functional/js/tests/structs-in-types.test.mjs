import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");
const structures = module.PlainDataStructuresFromTypeCollection;

test("creates and swaps type-collection points", () => {
  const point = structures.createPoint(1.0, 2.0);
  assert.deepEqual(point, { x: 1.0, y: 2.0 });

  assert.deepEqual(structures.swapPointCoordinates(point), { x: 2.0, y: 1.0 });
});


test("converts nested type-collection structs recursively", () => {
  const line = structures.createLine({ x: 1.0, y: 2.0 }, { x: 3.0, y: 4.0 });
  assert.deepEqual(line, {
    a: { x: 1.0, y: 2.0 },
    b: { x: 3.0, y: 4.0 },
  });

  assert.deepEqual(
    structures.createColoredLine(line, { red: 10, green: 20, blue: 30 }),
    {
      line,
      color: { red: 10, green: 20, blue: 30 },
    },
  );
});

test("converts all type-collection fields through a nested method signature", () => {
  const input = {
    int8Field: -1,
    uint8Field: 2,
    int16Field: -3,
    uint16Field: 4,
    int32Field: -5,
    uint32Field: 6,
    int64Field: -7n,
    uint64Field: 8n,
    floatField: 1.5,
    doubleField: 2.5,
    stringField: "value",
    booleanField: true,
    pointField: { x: 9.0, y: 10.0 },
  };

  assert.deepEqual(structures.modifyAllTypesStruct(input), {
    int8Field: 0,
    uint8Field: 3,
    int16Field: -2,
    uint16Field: 5,
    int32Field: -4,
    uint32Field: 7,
    int64Field: -6n,
    uint64Field: 9n,
    floatField: 2.5,
    doubleField: 3.5,
    stringField: "Hello value",
    booleanField: false,
    pointField: { x: 10.0, y: 9.0 },
  });
});