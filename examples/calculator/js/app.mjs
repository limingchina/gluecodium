import createModule from "./generated.mjs";

const display = document.querySelector("#display");
const expressionOutput = document.querySelector("#expression");
const keypad = document.querySelector("#keypad");
const clearButton = document.querySelector("#clear");
const historyList = document.querySelector("#history-list");

let calculator;
let module;
let multiplyCallbackType;
let currentInput = "0";
let storedValue = null;
let pendingOperator = null;
let waitingForOperand = false;
let justEvaluated = false;

function errorName(error) {
  const match = Object.entries(module.CalculatorError).find(([, value]) => value === error);
  return match ? match[0].replaceAll("_", " ").toLowerCase() : "calculation error";
}

function updateDisplay() {
  display.textContent = currentInput;
  expressionOutput.textContent = pendingOperator && storedValue !== null
    ? `${storedValue} ${pendingOperator}`
    : justEvaluated
      ? "Result"
      : "Ready";
}

function addHistory(expression, value) {
  const emptyItem = historyList.querySelector(".empty-history");
  emptyItem?.remove();

  const item = document.createElement("li");
  item.innerHTML = `<span>${expression}</span><strong>${value}</strong>`;
  historyList.prepend(item);

  while (historyList.children.length > 5) {
    historyList.lastElementChild.remove();
  }
}

function calculate(first, operator, second) {
  if (operator === "+") {
    const result = calculator.summarize(first, second);
    if (result.value === undefined) {
      throw new Error(errorName(result.error));
    }
    return result.value;
  }

  if (operator === "-") {
    let callbackResult;
    calculator.subtract(first, second, (error, result) => {
      callbackResult = error == null ? result : null;
    });
    if (callbackResult === null) {
      throw new Error("calculation error");
    }
    return callbackResult;
  }

  if (operator === "×") {
    let callbackResult;
    const callback = new multiplyCallbackType();
    callback.onError = (error) => {
      callbackResult = { error: errorName(error) };
    };
    callback.onResult = (result) => {
      callbackResult = { value: result };
    };
    calculator.multiply(first, second, callback);
    callback.delete();
    if (callbackResult.error) {
      throw new Error(callbackResult.error);
    }
    return callbackResult.value;
  }

  if (operator === "÷") {
    const result = calculator.divide({ dividend: first, divider: second });
    if (result.error !== undefined) {
      throw new Error(errorName(result.error));
    }
    return result.result;
  }

  throw new Error("Choose a calculator operation.");
}

function resetCalculator() {
  currentInput = "0";
  storedValue = null;
  pendingOperator = null;
  waitingForOperand = false;
  justEvaluated = false;
  updateDisplay();
}

function inputDigit(digit) {
  if (waitingForOperand || justEvaluated) {
    currentInput = digit;
    waitingForOperand = false;
    justEvaluated = false;
  } else {
    currentInput = currentInput === "0" ? digit : `${currentInput}${digit}`;
  }
  updateDisplay();
}

function inputDecimal() {
  if (waitingForOperand || justEvaluated) {
    currentInput = "0.";
    waitingForOperand = false;
    justEvaluated = false;
  } else if (!currentInput.includes(".")) {
    currentInput += ".";
  }
  updateDisplay();
}

function inputSign() {
  currentInput = currentInput.startsWith("-")
    ? currentInput.slice(1)
    : currentInput === "0"
      ? "0"
      : `-${currentInput}`;
  updateDisplay();
}

function chooseOperator(operator) {
  if (pendingOperator && !waitingForOperand) {
    evaluate();
  }
  storedValue = Number(currentInput);
  pendingOperator = operator;
  waitingForOperand = true;
  justEvaluated = false;
  updateDisplay();
}

function evaluate() {
  if (pendingOperator === null || storedValue === null || waitingForOperand) {
    return;
  }

  const first = storedValue;
  const second = Number(currentInput);
  const operator = pendingOperator;
  const result = calculate(first, operator, second);
  const value = String(result);
  addHistory(`${first} ${operator} ${second}`, value);
  currentInput = value;
  storedValue = null;
  pendingOperator = null;
  waitingForOperand = false;
  justEvaluated = true;
  updateDisplay();
}

function backspace() {
  if (waitingForOperand || justEvaluated) {
    return;
  }
  currentInput = currentInput.length > 1 ? currentInput.slice(0, -1) : "0";
  if (currentInput === "-") {
    currentInput = "0";
  }
  updateDisplay();
}

function handleInput(value) {
  try {
    if (/^\d$/.test(value)) {
      inputDigit(value);
    } else if (value === ".") {
      inputDecimal();
    } else if (value === "±") {
      inputSign();
    } else if (value === "⌫") {
      backspace();
    } else if (value === "C") {
      resetCalculator();
    } else if (["+", "-", "×", "÷"].includes(value)) {
      chooseOperator(value);
    } else if (value === "=") {
      evaluate();
    }
  } catch (error) {
    currentInput = "Error";
    storedValue = null;
    pendingOperator = null;
    waitingForOperand = true;
    justEvaluated = false;
    expressionOutput.textContent = error.message;
    display.textContent = currentInput;
  }
}

try {
  if (!globalThis.crossOriginIsolated) {
    throw new Error("The page needs COOP and COEP headers for WebAssembly threads.");
  }

  module = await createModule();
  calculator = module.Calculator.make();
  multiplyCallbackType = module.MultiplyCallback.extend("BrowserMultiplyCallback", {
    onError() {},
    onResult() {},
  });

  updateDisplay();

  keypad.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (button) {
      handleInput(button.dataset.value);
    }
  });

  clearButton.addEventListener("click", () => {
    historyList.innerHTML = '<li class="empty-history">No calculations yet.</li>';
    resetCalculator();
  });

  document.addEventListener("keydown", (event) => {
    const keyMap = { "*": "×", "/": "÷", Enter: "=", Escape: "C", Backspace: "⌫" };
    const value = keyMap[event.key] || event.key;
    if (/^\d$/.test(value) || [".", "±", "⌫", "C", "+", "-", "×", "÷", "="].includes(value)) {
      event.preventDefault();
      handleInput(value);
    }
  });
} catch (error) {
  display.textContent = "Error";
  expressionOutput.textContent = `Unable to load the WebAssembly module: ${error.message}`;
  console.error(error);
}

window.addEventListener("pagehide", () => calculator?.delete(), { once: true });
