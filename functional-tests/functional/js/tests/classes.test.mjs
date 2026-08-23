import assert from "node:assert/strict";
import test from "node:test";
import { pathToFileURL } from "node:url";

const modulePath = process.env.GLUECODIUM_JS_MODULE;
assert.ok(modulePath, "GLUECODIUM_JS_MODULE must point to the generated module");

const { default: createModule } = await import(pathToFileURL(modulePath));
const module = await createModule();

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