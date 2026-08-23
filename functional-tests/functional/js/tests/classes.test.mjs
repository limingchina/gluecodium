import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

const instancesFactory = module.InstancesFactory;
const simpleInstantiableOne = module.SimpleInstantiableOne;
const nestedInstantiableOne = module.NestedInstantiableOne;

test("creates and mutates class instances", () => {
  const instance = simpleInstantiableOne.create("initial");
  assert.equal(instance.getStringValue(), "initial");

  instance.setStringValue("updated");
  assert.equal(instance.getStringValue(), "updated");
  instance.delete();
});

test("preserves shared instances through nested class values", () => {
  const first = instancesFactory.createSimpleInstantiableOne();
  const second = simpleInstantiableOne.create("second");
  const nested = nestedInstantiableOne.create();

  nested.setSameTypeInstances(first, second);
  assert.equal(nested.getInstanceOne().isAliasOf(first), true);
  assert.equal(nested.getInstanceTwo().isAliasOf(second), true);

  nested.delete();
  first.delete();
  second.delete();
});