import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("round-trips primitive and nested primitive aliases", () => {
  assert.equal(module.StaticTypedef.returnIntTypedef(2), 3);
  assert.equal(module.StaticTypedef.returnNestedIntTypedef(4), 5);
  assert.equal(module.StaticTypedef.returnStringTypedef("world"), "Hello world");
});

test("round-trips blob aliases", () => {
  assert.deepEqual(
    [...module.StaticTypedef.returnByteBufferTypedef(new Uint8Array([1, 2, 3]))],
    [3, 2, 1],
  );
});

test("round-trips type-collection and struct aliases", () => {
  const point = module.StaticTypedef.returnTypedefPointFromTypeCollection({ x: 1, y: 3 });
  assert.deepEqual(point, { x: 1, y: 3 });

  const result = module.StaticTypedef.returnExampleStructTypedef({ exampleString: "world" });
  assert.equal(result.exampleString, "Hello world");

  const nestedResult = module.StaticTypedef.returnNestedStructTypedef({ exampleString: "world" });
  assert.equal(nestedResult.exampleString, "Hello world");
});