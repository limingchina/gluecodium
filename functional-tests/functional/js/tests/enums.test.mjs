import assert from "node:assert/strict";
import test from "node:test";
import { pathToFileURL } from "node:url";

const modulePath = process.env.GLUECODIUM_JS_MODULE;
assert.ok(modulePath, "GLUECODIUM_JS_MODULE must point to the generated module");

const { default: createModule } = await import(pathToFileURL(modulePath));
const module = await createModule();
const enums = module.Enums;
const internalError = module.test_EnumsInternalErrorType;

test("enum members are exported and round-trip", () => {
  assert.ok(internalError.ERROR_NONE !== undefined);
  assert.ok(internalError.ERROR_FATAL !== undefined);
  assert.equal(enums.flipEnumValue(internalError.ERROR_FATAL), internalError.ERROR_NONE);
  assert.equal(enums.flipEnumValue(internalError.ERROR_NONE), internalError.ERROR_FATAL);
});

test("enum values in type collections round-trip", () => {
  const typeCollection = module.EnumsTypeCollectionMethods;
  const collectionError = module.InternalErrorTypeCollection;

  assert.equal(
    typeCollection.flipEnumValue(collectionError.ERROR_FATAL),
    collectionError.ERROR_NONE,
  );
});