import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("dispatches overloads inherited by an interface", () => {
  const Interface = module.ChildInterfaceOverloads.extend("JavaScriptChildInterfaceOverloads", {
    foo(...args) {
      return args.length === 0 ? "foo()" : `foo(${args[0]})`;
    },
    bar(...args) {
      return args.length === 0 ? "bar()" : `bar(${args[0]})`;
    },
    baz() {
      return "baz()";
    },
  });
  const instance = new Interface();

  assert.equal(instance.foo(), "foo()");
  assert.equal(instance.foo("value"), "foo(value)");
  assert.equal(instance.bar(), "bar()");
  assert.equal(instance.bar("value"), "bar(value)");
  assert.equal(instance.baz(), "baz()");

  instance.delete();
});

test("registers overloads inherited by a class", () => {
  const instance = module.InheritanceOverloadsTestHelper.createClassOverloads();

  assert.doesNotThrow(() => instance.foo());
  assert.doesNotThrow(() => instance.foo(7));
  assert.doesNotThrow(() => instance.foo("value"));
  assert.doesNotThrow(() => instance.bar());
  assert.doesNotThrow(() => instance.bar("value"));
  assert.doesNotThrow(() => instance.baz());

  instance.delete();
});