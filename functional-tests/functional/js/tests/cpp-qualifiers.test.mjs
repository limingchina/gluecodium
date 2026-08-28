import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("dispatches const-qualified class methods", () => {
  const instance = module.CppConstClass.create();
  assert.equal(instance.getFoo(), "foo");
  instance.delete();
});

test("dispatches const and noexcept interface and inherited paths", () => {
  const constInterface = module.CppConstInterfaceFactory.createCppConstInterface();
  assert.equal(constInterface.getFoo(), "foo");
  assert.equal(module.CppConstInterfaceFactory.callGetFoo(constInterface), "foo");
  constInterface.delete();

  const inheritedClass = module.CppNoexceptClassInherited.create();
  assert.equal(inheritedClass.getFoo(), "foo");
  assert.equal(inheritedClass.getBar(), "bar");
  assert.equal(inheritedClass.stringProperty, "foo");
  inheritedClass.delete();

  const inheritedInterface =
    module.CppNoexceptInterfaceFactory.createCppNoexceptInheritedInterface();
  assert.equal(inheritedInterface.getFoo(), "foo");
  assert.equal(inheritedInterface.getBar(), "bar");
  assert.equal(inheritedInterface.stringProperty, "foo");
  inheritedInterface.delete();

  assert.equal(module.CppNoexceptInterfaceFactory.stringProperty, "foo");
});