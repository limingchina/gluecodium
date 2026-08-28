import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");
const inheritanceHelper = module.InheritanceTestHelper;

test("dispatches overridden methods through inherited interfaces", () => {
  const instance = inheritanceHelper.createChild();

  inheritanceHelper.callRootMethod(instance, "inherited call");
  assert.equal(instance.getData(), "C++ Child data is 'inherited call'");

  instance.delete();
});

test("preserves multi-level class inheritance", () => {
  const instance = module.GrandchildClass.createGrandchildClass();

  assert.equal(typeof instance.doSomethingToChildClass, "function");
  instance.childNumber = 7;
  assert.equal(instance.childNumber, 7);

  instance.delete();
});

test("returns derived instances through their inherited interface", () => {
  const instance = inheritanceHelper.createConcreteChildAsChildInterface();

  inheritanceHelper.callRootMethod(instance, "interface return");
  assert.equal(instance.getData(), "C++ ConcreteChild data is 'interface return'");

  instance.delete();
});