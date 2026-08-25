import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const external = await loadPackage("external");
const module = await loadPackage("test");

test("exports external types through the public package facade", () => {
  assert.ok(external.ExternalStruct);
  assert.ok(external.AnotherExternalStruct);
  assert.ok(external.ExternalEnum.FOO);
  assert.ok(external.ExternalEnum.BAR);
});

test("round-trips external struct fields and accessors", () => {
  const value = {
    stringField: "plain",
    externalStringField: "external",
    externalArrayField: [1, 2, 3],
    externalStructField: { intField: 42 },
  };

  const roundTripped = module.UseExternalTypes.extractExternalStruct({
    structField: value,
    enumField: external.ExternalEnum.BAR,
  });

  assert.deepEqual(roundTripped, value);
});

test("extracts external nested structs and enums", () => {
  const nestedStruct = {
    structField: {
      stringField: "plain",
      externalStringField: "external",
      externalArrayField: [],
      externalStructField: { intField: 7 },
    },
    enumField: external.ExternalEnum.FOO,
  };

  assert.deepEqual(
    module.UseExternalTypes.extractAnotherExternalStruct(nestedStruct),
    { intField: 7 },
  );
  assert.equal(
    module.UseExternalTypes.extractExternalEnum(nestedStruct),
    external.ExternalEnum.FOO,
  );
});