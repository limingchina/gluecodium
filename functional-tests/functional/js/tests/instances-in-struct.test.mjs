import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");
const instances = module.InstanceInStruct;

test("preserves nested class instances through struct values", () => {
  const holder = instances.createInStruct();
  assert.equal(holder.mySelf.getStringValue(), "foo");

  holder.mySelf.setStringValue("updated");
  assert.equal(holder.mySelf.getStringValue(), "updated");
});

test("handles nullable and non-nullable nested class fields", () => {
  assert.equal(instances.createNullInStruct().mySelf, null);
  assert.equal(instances.createInNotNullStruct().mySelf.getStringValue(), "foo");
  assert.equal(instances.createInEmptyNotNullStruct().mySelf, null);
});