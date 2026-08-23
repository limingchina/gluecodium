import createModule from "./generated.mjs";

const form = document.querySelector("#calculator-form");
const firstNumber = document.querySelector("#first-number");
const secondNumber = document.querySelector("#second-number");
const calculateButton = document.querySelector("#calculate");
const resultOutput = document.querySelector("#result");

let calculator;

try {
  if (!globalThis.crossOriginIsolated) {
    throw new Error("The page needs COOP and COEP headers for WebAssembly threads.");
  }

  const module = await createModule();
  calculator = module.Calculator.make();

  calculateButton.disabled = false;
  calculateButton.textContent = "Calculate sum";
  resultOutput.textContent = "Ready";

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const first = Number(firstNumber.value);
    const second = Number(secondNumber.value);
    if (!Number.isFinite(first) || !Number.isFinite(second)) {
      resultOutput.textContent = "Enter two numbers.";
      return;
    }

    const result = calculator.summarize(first, second);
    resultOutput.textContent = `${first} + ${second} = ${result.value}`;
  });
} catch (error) {
  calculateButton.textContent = "Calculator unavailable";
  resultOutput.textContent = `Unable to load the WebAssembly module: ${error.message}`;
  console.error(error);
}

window.addEventListener("pagehide", () => calculator?.delete(), { once: true });
