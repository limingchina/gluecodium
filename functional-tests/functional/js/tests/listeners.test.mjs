import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("round-trips JavaScript listeners through native code", () => {
  const Listener = module.SomeSimpleInterface.extend("JavaScriptSomeSimpleInterface", {});
  Object.defineProperty(Listener.prototype, "value", {
    get() {
      return "listener value";
    },
  });
  const listener = new Listener();
  const result = module.SomeSimpleRoundTrip.roundTrip(listener);

  assert.equal(result.value, "listener value");

  result.delete();
  listener.delete();
});

test("dispatches JavaScript interface properties", () => {
  const PropertyInterface = module.InterfaceWithProperty.extend("JavaScriptInterfaceWithProperty", {});
  Object.defineProperty(PropertyInterface.prototype, "stringProperty", {
    get() {
      return this.value;
    },
    set(value) {
      this.value = value;
    },
  });
  const instance = new PropertyInterface();

  instance.stringProperty = "property value";
  assert.equal(instance.stringProperty, "property value");
  instance.delete();
});

test("round-trips a native listener implementation", () => {
  const listener = module.ForecastFactory.createListener();
  const provider = module.ForecastFactory.createProvider();

  provider.inform(listener);
  assert.equal(
    module.ForecastFactory.getLog(),
    "Berlin -> [-2, 26]\nMadrid -> [1, 33]\nMarrakesh -> [8, 40]\n",
  );

  provider.delete();
  listener.delete();
});
