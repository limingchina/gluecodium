import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");
const dates = module.Dates;
const increment = 24 * 60 * 60 * 1000 + 60 * 60 * 1000 + 60 * 1000 + 1000;

test("increases dates before and after the Unix epoch", () => {
  for (const milliseconds of [-2208988800000, 0, 1700000000123]) {
    const input = new Date(milliseconds);
    const result = dates.increaseDate(input);

    assert.ok(result instanceof Date);
    assert.equal(result.getTime(), milliseconds + increment);
  }
});

test("round-trips nullable dates", () => {
  assert.equal(dates.increaseDateMaybe(null), undefined);

  const input = new Date(123456789);
  assert.equal(dates.increaseDateMaybe(input).getTime(), input.getTime() + increment);
});

test("round-trips dates in sets", () => {
  const input = new Date(987654321);

  dates.dateSet = new Set([input, new Date(-123456789)]);
  assert.deepEqual(
    [...dates.dateSet].map((date) => date.getTime()).sort((left, right) => left - right),
    [-123456789, 987654321],
  );
});

test("round-trips the adapted static date property", () => {
  const input = new Date(-86400000);

  dates.dateAttribute = input;

  assert.equal(dates.dateAttribute.getTime(), input.getTime());
});