import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("loads mutually dependent declarations and their generated surfaces", () => {
  assert.equal(typeof module.Alice, "function");
  assert.equal(typeof module.Bob, "function");
  assert.equal(typeof module.Alice.prototype.meetBob, "function");
  assert.equal(typeof module.Bob.prototype.meetAlice, "function");
  assert.equal(typeof module.Alice.prototype.delete, "function");
  assert.equal(typeof module.Bob.prototype.delete, "function");
});