import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("exports nested classes, structs, enums, typedefs, and lambdas", () => {
  assert.equal(typeof module.OuterClassInnerClass, "function");
  assert.equal(typeof module.OuterClassInnerStruct, "object");
  assert.equal(typeof module.OuterClassInnerEnum, "function");
  assert.equal(typeof module.LevelFour, "object");
  assert.equal(module.LevelFour.FOO, false);
  assert.equal(typeof module.LevelFour.fooFactory, "function");
  assert.deepEqual(module.LevelFour.fooFactory(), { stringField: "" });

  assert.equal(typeof module.InterfaceRefersNestedTypedefAsReturnValue, "function");
  assert.equal(typeof module.InterfaceRefersNestedLambdaAsReturnValue, "function");
});

test("keeps colliding nested class exports distinct", () => {
  assert.notEqual(module.OuterClassInnerClass, module.OuterInterfaceInnerClass);
  assert.notEqual(module.OuterClassInnerClass, module.OuterStructInnerClass);
  assert.equal(typeof module.OuterInterfaceInnerClass, "function");
  assert.equal(typeof module.OuterStructInnerClass, "function");
});

test("dispatches nested interface implementations", () => {
  const NestedInterface = module.InnerInterface.extend("JavaScriptNestedInterface", {
    foo(input) {
      return `nested:${input}`;
    },
  });
  const instance = new NestedInterface();

  assert.equal(instance.foo("value"), "nested:value");
  instance.delete();
});

test("converts nested class properties and nested struct functions", () => {
  const venue = module.VenueGeometry.create();
  assert.equal(venue.internalAddress.longAddress, "foobar");
  venue.delete();

  assert.deepEqual([...module.OuterStructInnerClass.fooBar()], [42]);
});

test("wraps errors from nested struct functions", () => {
  assert.throws(
    () => module.OuterStruct.doNothing(),
    (error) => error.name === "InstantiationError" && error.error === 1,
  );
});