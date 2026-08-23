import assert from "node:assert/strict";
import test from "node:test";
import { pathToFileURL } from "node:url";

const modulePath = process.env.GLUECODIUM_JS_MODULE;
assert.ok(modulePath, "GLUECODIUM_JS_MODULE must point to the generated module");

const { default: createModule } = await import(pathToFileURL(modulePath));
const module = await createModule();
const structures = module.PlainDataStructures;

test("creates and swaps points", () => {
  const point = structures.createPoint(1.0, 2.0);
  assert.equal(point.x, 1.0);
  assert.equal(point.y, 2.0);

  const swapped = structures.swapPointCoordinates(point);
  assert.equal(swapped.x, 2.0);
  assert.equal(swapped.y, 1.0);
});

test("maps nested structs and value fields", () => {
  const line = structures.createLine({ x: 1.0, y: 2.0 }, { x: 3.0, y: 4.0 });
  assert.equal(line.a.x, 1.0);
  assert.equal(line.b.y, 4.0);

  const colored = structures.createColoredLine(line, { red: 10, green: 20, blue: 30 });
  assert.equal(colored.color.red, 10);
  assert.equal(colored.line.b.x, 3.0);
});

test("allows struct field mutation", () => {
  const point = structures.createPoint(0.0, 0.0);
  point.x = 5.0;
  assert.equal(point.x, 5.0);
});