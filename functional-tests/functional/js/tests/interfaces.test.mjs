import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

const interfacesFactory = module.InterfacesFactory;

test("dispatches calls on native interface implementations", () => {
  const instance = interfacesFactory.createSimpleInterfaceOne();

  instance.setStringValue("native value");
  assert.equal(instance.getStringValue(), "native value");
  instance.delete();
});

test("round-trips JavaScript interface implementations", () => {
  const FirstInterface = module.SimpleInterfaceOne.extend("JavaScriptSimpleInterfaceOne", {
    setStringValue(value) {
      this.value = value;
    },
    getStringValue() {
      return this.value;
    },
  });
  const SecondInterface = module.SimpleInterfaceOne.extend("JavaScriptSimpleInterfaceTwo", {
    setStringValue(value) {
      this.value = value;
    },
    getStringValue() {
      return this.value;
    },
  });
  const first = new FirstInterface();
  const second = new SecondInterface();
  const nested = interfacesFactory.createNestedInterfaceOne();

  first.setStringValue("first value");
  second.setStringValue("second value");
  nested.setSameTypeInterfaces(first, second);

  assert.equal(nested.getInterfaceOne().getStringValue(), "first value");
  assert.equal(nested.getInterfaceTwo().getStringValue(), "second value");

  nested.delete();
  first.delete();
  second.delete();
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