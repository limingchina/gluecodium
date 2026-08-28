import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");
const equatable = module.Equatable;
const equatableClass = module.EquatableClass;
const pointerEquatableClass = module.PointerEquatableClass;
const someEnum = module.SomeSomeEnum;

function createEquatableStruct() {
  return {
    boolField: true,
    intField: 42,
    longField: 7n,
    floatField: 1.5,
    doubleField: 2.5,
    stringField: "value",
    structField: { fooField: "nested" },
    immutableStructField: { fooField: "immutable" },
    enumField: someEnum.FOO,
    mapField: new Map([[1, "one"]]),
    arrayField: ["one", "two"],
  };
}

function createNullableStruct() {
  return {
    boolField: false,
    intField: 0,
    uintField: 7,
    floatField: 0,
    stringField: "",
    structField: { fooField: "nested" },
    enumField: someEnum.BAR,
    mapField: new Map(),
    arrayField: [],
  };
}

test("compares equatable structs and their nested values", () => {
  const first = createEquatableStruct();
  const second = createEquatableStruct();

  assert.equal(equatableClass.areEqual(first, second), true);
  assert.equal(equatableClass.haveSameHash(first, second), true);

  second.structField.fooField = "changed";
  assert.equal(equatableClass.areEqual(first, second), false);

  second.structField.fooField = "nested";
  second.immutableStructField.fooField = "changed";
  assert.equal(equatableClass.areEqual(first, second), false);
});

test("compares nullable and immutable equatable structs", () => {
  const first = createNullableStruct();
  const second = createNullableStruct();

  assert.equal(equatableClass.areEqual(first, second), true);
  assert.equal(equatableClass.haveSameHash(first, second), true);

  second.mapField = null;
  assert.equal(equatableClass.areEqual(first, second), false);

});

test("preserves equality for equatable pointer fields", () => {
  const first = pointerEquatableClass.createNew();
  const same = pointerEquatableClass.returnLast();
  const second = pointerEquatableClass.createNew();

  assert.equal(first.isAliasOf(same), true);
  assert.equal(first.isAliasOf(second), false);

  const value = { equatable: equatableClass.create("value"), pointerEquatable: first };
  const copy = { equatable: value.equatable, pointerEquatable: same };
  assert.equal(pointerEquatableClass.areEqual(value, copy), true);
  assert.equal(pointerEquatableClass.haveSameHash(value, copy), true);

  value.equatable.delete();
  first.delete();
  second.delete();
});

test("preserves referential equality for equatable interface instances", () => {
  const first = module.EquatableInterfaceFactory.createEquatableInterface("same");
  const second = module.EquatableInterfaceFactory.createEquatableInterface("same");

  assert.equal(first.isAliasOf(first), true);
  assert.equal(first.isAliasOf(second), false);

  first.delete();
  second.delete();
});