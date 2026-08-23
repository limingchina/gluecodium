import createModule from "./pthreads_callbacks_spike.mjs";

const Module = await createModule();
Module.invokeFromWorker((value) => `js-${value}`);

console.log("Unexpectedly invoked a cross-thread emscripten::val");