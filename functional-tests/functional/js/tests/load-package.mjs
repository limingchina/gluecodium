import assert from "node:assert/strict";
import { dirname, resolve } from "node:path";
import { pathToFileURL } from "node:url";

export async function loadPackage(packagePath) {
  const modulePath = process.env.GLUECODIUM_JS_MODULE;
  assert.ok(modulePath, "GLUECODIUM_JS_MODULE must point to the generated module");
  return import(pathToFileURL(resolve(dirname(modulePath), "js", packagePath, "index.mjs")));
}