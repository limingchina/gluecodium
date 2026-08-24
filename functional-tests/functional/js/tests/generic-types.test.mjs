import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("round-trips primitive arrays and nested arrays", () => {
  assert.deepEqual(module.Arrays.reverseStringArray(["one", "two"]), ["two", "one"]);
  assert.deepEqual(module.Arrays.reverseArrayInline([1, 2, 3]), [3, 2, 1]);
  assert.deepEqual(
    module.Arrays.reverseNestedPrimitiveArray([[1, 2], [3, 4]]),
    [[4, 3], [2, 1]],
  );
});

test("round-trips maps and maps of arrays", () => {
  assert.deepEqual(
    module.Maps.methodWithMap(new Map([[1, "one"], [2, "two"]])),
    new Map([[1, "ONE"], [2, "TWO"]]),
  );
  assert.deepEqual(
    module.Maps.methodWithMapOfArrays(new Map([[1, ["one", "two"]]])),
    new Map([[1, ["ONE", "TWO"]]]),
  );
});

test("round-trips sets", () => {
  assert.deepEqual(
    module.SetType.stringSetRoundTrip(new Set(["one", "two"])),
    new Set(["one", "two"]),
  );
  assert.deepEqual(
    module.SetType.nullableIntSetRoundTrip(new Set([1, 2, 3])),
    new Set([1, 2, 3]),
  );
});

test("round-trips nested generic containers", () => {
  assert.deepEqual(
    module.NestedGenericTypes.methodWithListOfLists([[1, 2], [3, 4]]),
    [[1, 2], [3, 4]],
  );
  assert.deepEqual(
    module.NestedGenericTypes.methodWithListAndMap([
      new Map([[1, true], [2, false]]),
    ]),
    new Map([[1, [1]], [2, [0]]]),
  );
});