import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("round-trips locale tags as strings", () => {
  assert.equal(module.Locales.localeRoundTrip("en-US"), "en-US");
  assert.equal(module.Locales.localeRoundTrip("sr-Cyrl"), "sr-Cyrl");
  assert.equal(module.Locales.localeRoundTripStripTag("en-US"), "und");
});

test("round-trips nullable locales and locale properties", () => {
  assert.equal(module.Locales.localeRoundTripNullable("en-US"), "en-US");
  assert.equal(module.Locales.localeRoundTripNullable(null), undefined);

  module.Locales.localeProperty = "fr-CA";
  assert.equal(module.Locales.localeProperty, "fr-CA");
});

test("converts locale value objects and defaults", () => {
  const result = module.LocalesStruct.localesStructRoundTrip({
    primaryLocale: "en-US",
    secondaryLocale: "fr-CA",
  });
  assert.equal(result.primaryLocale, "en-US");
  assert.equal(result.secondaryLocale, "fr-CA");

  const defaults = module.LocaleDefaults.getCppDefaults();
  assert.equal(defaults.english, "en");
  assert.equal(defaults.latAmSpanish, "es-419");
  assert.equal(defaults.serbianCyrillic, "sr-Cyrl");
  assert.equal(defaults.traditionalChineseTaiwan, "nan-Hant-TW");
});

test("converts locale collections", () => {
  assert.deepEqual(
    module.LocaleGenerics.localeListRoundTrip(["en-US", "fr-CA"]),
    ["en-US", "fr-CA"],
  );
  assert.deepEqual(
    [...module.LocaleGenerics.localeSetRoundTrip(new Set(["en-US", "fr-CA"]))].sort(),
    ["en-US", "fr-CA"],
  );
  assert.deepEqual(
    [...module.LocaleGenerics.localeKeysMapRoundTrip(new Map([["en-US", "English"]]))],
    [["en-US", "English"]],
  );
  assert.deepEqual(
    [...module.LocaleGenerics.localeValuesMapRoundTrip(new Map([["greeting", "en-US"]]))],
    [["greeting", "en-US"]],
  );
});