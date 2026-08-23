import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("static string methods round-trip values", () => {
  const methods = module.StaticStringMethods;

  assert.equal(methods.returnInputString("abc"), "abc");
  assert.equal(methods.concatenateStrings("a", "b"), "ab");
  assert.equal(methods.returnHelloString(), "hello");
  assert.equal(methods.returnEmpty(), "");
});

test("C string parameters and returns are converted", () => {
  const methods = module.StringsWithCstring;

  assert.equal(methods.returnInputStringType("x"), "x");
  assert.equal(methods.returnInputString("y"), "y");
});

test("reference-returned strings are readable", () => {
  const type = module.CppRefReturnType;

  assert.equal(type.stringRef(), "nonsense");
  assert.equal(type.stringProperty(), "nonsense");
});