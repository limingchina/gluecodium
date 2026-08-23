import createModule from "./pthreads_callbacks_spike.mjs";

const Module = await createModule();
const pump = setInterval(() => Module.pumpRuntimeQueue(), 0);
const toResult = (callback) => (...args) => {
	try {
		return { ok: true, value: callback(...args) };
	} catch (error) {
		return { ok: false, error: error instanceof Error ? error.message : String(error) };
	}
};
const result = await new Promise((resolve, reject) => {
	Module.invokeFromWorkerAsync(toResult((value) => `js-${value}`), resolve, reject);
});

if (result !== "js-worker") {
	throw new Error(`unexpected callback result: ${result}`);
}

const rejection = await new Promise((resolve) => {
	Module.invokeFromWorkerAsync(
		toResult(() => {
			throw new Error("callback failure");
		}),
		() => resolve("resolved"),
		(error) => resolve(error),
	);
});
if (rejection !== "callback failure") {
	throw new Error(`unexpected callback rejection: ${rejection}`);
}
clearInterval(pump);
console.log("PASS: callback marshalled to the runtime thread");