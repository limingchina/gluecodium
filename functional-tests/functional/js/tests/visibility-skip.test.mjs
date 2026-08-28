import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("hides internal declarations from the public package", () => {
  assert.equal(typeof module.SomeClassWithInternalMembers, "function");
  assert.equal(typeof module.SomeClassWithInternalMembers.create, "function");
  assert.equal(module.SomeClassWithInternalMembers.someInternalFunction, undefined);
  assert.equal(module.SomeClassWithInternalMembers.someInternalProperty, undefined);
  assert.equal(module.InternalAttributeClassWithFunctions, undefined);
  assert.equal(module.InternalClassWithFunctions, undefined);
  assert.equal(module.JavaPublicClass, undefined);
  assert.equal(typeof module.JavaInternalClass, "function");
  assert.equal(module.DartPublicClass, undefined);
  assert.equal(typeof module.DartInternalClass, "function");
});

test("honors platform-independent skip tags", () => {
  assert.equal(typeof module.SkipTagsOnly, "function");
  assert.equal(module.SkipTagsOnly.skipUnquoted, undefined);
  assert.equal(module.SkipTagsOnly.skipQuoted, undefined);
  assert.equal(module.SkipMe, undefined);
  assert.equal(module.SkipMeToo, undefined);
  assert.equal(typeof module.SkipField, "object");
  assert.equal(module.SkipField.prototype?.noField, undefined);
});

test("retains enabled tags and omits disabled tags", () => {
  assert.equal(typeof module.EnableIfEnabled, "function");
  assert.equal(typeof module.EnableIfEnabled.enableUnquoted, "function");
  assert.equal(typeof module.EnableIfEnabled.enableQuoted, "string");
  assert.equal(typeof module.EnableIfSkipped, "function");
  assert.equal(module.EnableIfSkipped.skipUnquoted, undefined);
  assert.equal(module.EnableIfSkipped.skipQuoted, undefined);
  assert.equal(module.SkippedMe, undefined);
  assert.equal(module.SkippedMeToo, undefined);
});