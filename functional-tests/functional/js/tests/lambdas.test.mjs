import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("passes JavaScript lambdas into native code", () => {
  const result = module.Lambdas.concatenate("foo", "bar", (first, second) => `${first}>.<${second}`);

  assert.equal(result, "foo>.<bar");
});

test("passes a collection of JavaScript lambdas into native code", () => {
  const concatenator = (first, second) => first + second;
  const result = module.Lambdas.concatenateList(
    ["foo", ">.<", "bar"],
    [concatenator, concatenator],
  );

  assert.equal(result, "foo>.<bar");
});

test("supports nullable JavaScript lambdas", () => {
  const result = module.Lambdas.concatenateOrNot(
    "foo",
    "bar",
    (first, second) => `${first}>.<${second}`,
  );

  assert.equal(result, "foo>.<bar");
  assert.equal(module.Lambdas.concatenateOrNot("foo", "bar", undefined), undefined);
});

test("passes overloaded and struct-defined JavaScript lambdas into native code", () => {
  assert.equal(module.CallOverloadedLambda.invokeOverloadedLambda((value) => `${value}`, 42), "42");

  const result = module.StructWithLambda.invokeCallback((value) => value);
  assert.equal(result, "some callback argument");
});