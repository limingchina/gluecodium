import assert from "node:assert/strict";
import createModule from "./generated.mjs";

const module = await createModule();
const calculator = module.Calculator.make();

assert.deepEqual(calculator.summarize(20, 22), { value: 42 });
assert.deepEqual(calculator.divide({ dividend: 20, divider: 4 }), {
  error: undefined,
  result: 5,
});
assert.equal(calculator.max(3, 7), 7);
assert.equal(calculator.min(8, 3).getResult(), 3);
assert.ok(module.CalculatorError.RESULT_OUT_OF_BOUNDS);

calculator.delete();
console.log("Calculator JS smoke test OK");