import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");
const factory = module.MultipleInheritanceFactory;
const checker = module.MultipleInheritanceChecker;

test("flattens secondary interface members onto a class binding", () => {
  const instance = factory.getMultiClass();

  assert.equal(typeof instance.parentFunction, "function");
  assert.equal(typeof instance.parentFunctionLight, "function");
  assert.equal(typeof instance.childFunction, "function");
  assert.equal(instance.parentFunctionLight(), "foo class");
  instance.parentProperty;
  instance.parentPropertyLight;
  instance.childProperty;

  instance.delete();
});

test("flattens secondary interface members onto an interface binding", () => {
  const instance = factory.getMultiInterface();

  assert.equal(typeof instance.parentFunction, "function");
  assert.equal(typeof instance.parentFunctionLight, "function");
  assert.equal(typeof instance.childFunction, "function");
  assert.equal(instance.parentFunctionLight(), "foo interface");
  instance.parentProperty;
  instance.parentPropertyLight;
  instance.childProperty;

  instance.delete();
});

test("preserves primary-base casts and secondary-interface identity", () => {
  const instance = factory.getMultiInterface();
  assert.equal(checker.checkIsNarrow(instance), true);
  instance.delete();

  const narrow = factory.getMultiClassAsNarrow();
  assert.equal(typeof narrow.parentFunctionLight, "function");
  assert.equal(checker.checkIsMultiInterface(narrow), false);
  narrow.delete();

  const singleton = factory.getMultiClassSingleton();
  const roundTrip = checker.narrowRoundTrip(singleton);
  assert.equal(checker.checkSingletonEquality(roundTrip), true);
  assert.equal(checker.checkNarrowEquality(singleton, roundTrip), true);
  roundTrip.delete();
});