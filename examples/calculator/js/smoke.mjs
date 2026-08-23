import assert from "node:assert/strict";
import { dirname, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const { default: createModule } = await import(
  pathToFileURL(resolve(dirname(process.argv[1]), "generated.mjs"))
);

const module = await createModule();
const calculator = module.Calculator.make();
const multiplyCallbackType = module.MultiplyCallback.extend("SmokeMultiplyCallback", {
  onError() {},
  onResult() {},
});

assert.deepEqual(calculator.summarize(20, 22), { value: 42 });
let subtractResult;
calculator.subtract(20, 8, (error, result) => {
  subtractResult = { error, result };
});
assert.deepEqual(subtractResult, { error: undefined, result: 12 });

let multiplyResult;
const multiplyCallback = new multiplyCallbackType();
multiplyCallback.onError = (error) => {
  multiplyResult = { error };
};
multiplyCallback.onResult = (result) => {
  multiplyResult = { result };
};
calculator.multiply(6, 7, multiplyCallback);
multiplyCallback.delete();
assert.deepEqual(multiplyResult, { result: 42 });

assert.deepEqual(calculator.divide({ dividend: 20, divider: 4 }), {
  error: undefined,
  result: 5,
});
assert.equal(calculator.divide({ dividend: 20, divider: 0 }).error, module.CalculatorError.DIVIDE_BY_ZERO);
assert.equal(calculator.max(3, 7), 7);
assert.equal(calculator.max(null, 7), 7);
assert.equal(calculator.max(null, null), undefined);
const minimum = calculator.min(8, 3);
assert.equal(minimum.getResult(), 3);
minimum.delete();
assert.ok(module.CalculatorError.RESULT_OUT_OF_BOUNDS);

calculator.delete();
console.log("Calculator JS smoke test OK");