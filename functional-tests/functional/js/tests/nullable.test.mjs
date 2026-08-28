import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const testPackage = await loadPackage("test");
const nullable = testPackage.NullableInterface.create();
const someEnum = testPackage.NullableInterfaceSomeEnum;
const nullableStruct = testPackage.NullableInterfaceNullableStruct;
let listenerArrayAttribute;
const nullableListener = testPackage.NullableListener.extend("JavaScriptNullableListener", {
  methodWithDouble(value) {
    return value;
  },
});
Object.defineProperty(nullableListener.prototype, "arrayAttribute", {
  get() {
    return listenerArrayAttribute;
  },
  set(value) {
    listenerArrayAttribute = value;
  },
});

test("round-trips nullable scalar, enum, struct, and collection values", () => {
  assert.equal(nullable.methodWithString(null), undefined);
  assert.equal(nullable.methodWithString("value"), "value");
  assert.equal(nullable.methodWithBoolean(false), false);
  assert.equal(nullable.methodWithDouble(0), 0);
  assert.equal(nullable.methodWithInt(null), undefined);
  assert.equal(nullable.methodWithInt(42n), 42n);
  assert.equal(nullable.methodWithUint(null), undefined);
  assert.equal(nullable.methodWithSomeEnum(null), undefined);
  assert.equal(nullable.methodWithSomeEnum(someEnum.ON), someEnum.ON);
  assert.equal(nullable.methodWithSomeStruct(null), undefined);
  assert.deepEqual(nullable.methodWithSomeStruct({ stringField: "value" }), { stringField: "value" });
  assert.equal(nullable.methodWithSomeArray(null), undefined);
  assert.deepEqual(nullable.methodWithSomeArray(["one", "two"]), ["one", "two"]);
  assert.equal(nullable.methodWithInlineArray(null), undefined);
  assert.deepEqual(nullable.methodWithInlineArray(["one"]), ["one"]);
  assert.equal(nullable.methodWithSomeMap(null), undefined);
  assert.deepEqual([...nullable.methodWithSomeMap(new Map([[7n, "value"]]))], [[7n, "value"]]);
});

test("preserves nullable struct fields and zero values", () => {
  const empty = {};
  assert.equal(empty.stringField, undefined);
  assert.equal(empty.boolField, undefined);
  assert.equal(empty.doubleField, undefined);
  assert.equal(empty.structField, undefined);
  assert.equal(empty.enumField, undefined);
  assert.equal(empty.arrayField, undefined);
  assert.equal(empty.inlineArrayField, undefined);
  assert.equal(empty.mapField, undefined);
  assert.equal(empty.blobField, undefined);

  const value = {
    stringField: "",
    boolField: false,
    doubleField: 0,
    structField: { stringField: "nested" },
    enumField: someEnum.OFF,
    arrayField: [],
    inlineArrayField: [],
    mapField: new Map(),
    blobField: new Uint8Array(),
  };
  const result = nullable.methodWithNullableStruct(value);
  assert.equal(result.stringField, "");
  assert.equal(result.boolField, false);
  assert.equal(result.doubleField, 0);
  assert.deepEqual(result.structField, { stringField: "nested" });
  assert.equal(result.enumField, someEnum.OFF);
  assert.deepEqual(result.arrayField, []);
  assert.deepEqual(result.inlineArrayField, []);
  assert.deepEqual([...result.mapField], []);
  assert.deepEqual(Array.from(result.blobField), []);
});

test("round-trips nullable interface values and properties", () => {
  const listener = new nullableListener();
  assert.equal(testPackage.NullableInterface.nullableListenerMethodRoundTrip(listener, null), undefined);
  assert.equal(testPackage.NullableInterface.nullableListenerMethodRoundTrip(listener, 3.14), 3.14);
  assert.equal(testPackage.NullableInterface.nullableListenerAttributeRoundTrip(listener, null), undefined);
  assert.deepEqual(
    testPackage.NullableInterface.nullableListenerAttributeRoundTrip(listener, ["value"]),
    ["value"],
  );

  nullable.stringAttribute = "value";
  assert.equal(nullable.stringAttribute, "value");
  nullable.stringAttribute = null;
  assert.equal(nullable.stringAttribute, undefined);
  nullable.boolAttribute = false;
  assert.equal(nullable.boolAttribute, false);
  nullable.intAttribute = 42n;
  assert.equal(nullable.intAttribute, 42n);
  nullable.arrayAttribute = ["value"];
  assert.deepEqual(nullable.arrayAttribute, ["value"]);
  nullable.mapAttribute = new Map([[7n, "value"]]);
  assert.deepEqual([...nullable.mapAttribute], [[7n, "value"]]);
});