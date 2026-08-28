import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("exports declaration-order type carrier", () => {
  assert.equal(typeof module.DeclarationOrderWithFunctions, "object");
});

test("exports struct companion constants and functions", () => {
  assert.equal(module.SimpleRoute.DEFAULT_DESCRIPTION, "Nonsense");
  assert.equal(module.SimpleRoute.DEFAULT_TYPE, module.RouteType.EQUESTRIAN);
  assert.equal(module.SimpleRoute.getDefaultDescription(), "Nonsense");

  assert.equal(module.MultiRoute.DEFAULT_DESCRIPTION, "Foo");
  assert.equal(
    module.MultiRoute.DEFAULT_TYPE,
    module.RouteType.NONE,
  );
  assert.equal(
    module.MultiRoute.getDefaultDescription(),
    "Foo",
  );
});