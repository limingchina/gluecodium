# JavaScript/Embind Generator - Phase 7 Status

**Status**: Complete for CMake integration and the calculator end-to-end example

**Date**: 2026-08-23

**Commit**: `63a938bd5` - `Add CMake integration for JavaScript bindings`

## Scope Delivered

Phase 7 integrates the JavaScript/embind generator with the CMake build and establishes the first
end-to-end generated module. The implementation now provides:

- `js` in the CMake-supported generator list when an Emscripten toolchain is active;
- JS generator properties forwarded through CMake-driven Gluecodium generation;
- `cmake/modules/gluecodium/Js.cmake` with an Emscripten-only module target;
- generated embind unity sources tracked as build inputs, with generation ordered before compilation;
- generated C++ API headers exposed to the Emscripten target without adding embind outputs to host
  C++ targets;
- the calculator `js` target, gated by `ENABLE_JS=ON`;
- a Node.js smoke test at `examples/calculator/js/smoke.mjs`; and
- a browser example at `examples/calculator/js/index.html` and `examples/calculator/js/app.mjs`
  that creates and uses the generated `Calculator` class; and
- a `serve.py` helper copied into the build directory to serve the browser example with the
  required cross-origin isolation headers; and
- calculator README instructions for configuring and building with `emcmake`.

The supported build model is the Emscripten toolchain applied to the complete CMake configure.
The HERE SDK core, generated C++, and generated embind glue are therefore compiled together by
`em++`. A separate wasm-only super-build remains a possible future size optimization, not part of
Phase 7.

## Build and Use

With an activated Emscripten SDK, CMake, Ninja, and Node.js installed, run this from the repository
root:

```bash
rm -rf build-calculator-js
GLUECODIUM_PATH="$PWD" emcmake cmake \
  -S examples/calculator \
  -B build-calculator-js \
  -G Ninja \
  -DENABLE_APP=OFF \
  -DENABLE_JS=ON
GLUECODIUM_PATH="$PWD" cmake --build build-calculator-js --target mylibrary_js
node build-calculator-js/calculator-js-smoke.mjs
```

The generated module consists of `generated.mjs` and `generated.wasm`. It is a modularized ES
module and can be loaded from Node.js with:

```js
import createModule from "./generated.mjs";

const module = await createModule();
const calculator = module.Calculator.make();
const result = calculator.summarize(20, 22);
calculator.delete();
```

The generated declarations and package metadata remain in the JS package output. The calculator
build also copies `index.html`, `app.mjs`, and `serve.py` beside the generated module for browser
use. Embind class handles should be released with `.delete()` when they are no longer needed.

## Runtime Contract

The module is built with the following relevant flags:

```text
-lembind
-fexceptions
-pthread
-sWASM_BIGINT=1
-sPTHREAD_POOL_SIZE=4
-sMODULARIZE=1
-sEXPORT_ES6=1
-sENVIRONMENT=web,node
-sALLOW_MEMORY_GROWTH=1
--no-entry
```

`--no-entry` is required because the embind module has no handwritten `main()` function.
`PROXY_TO_PTHREAD` is not used: it is incompatible with this no-entry embind module shape. The
pthreads build still requires browser cross-origin isolation. Browser deployments must send:

- `Cross-Origin-Opener-Policy: same-origin`
- `Cross-Origin-Embedder-Policy: require-corp`

These headers make `SharedArrayBuffer` and WebAssembly pthreads available to the module.

## Verification

Phase 7 was verified with focused CMake coverage, a calculator Emscripten build, and the Node.js
smoke test. The generated module was imported successfully and its embind API was exercised at
runtime. The browser example uses the same generated `Calculator` class and documents the
cross-origin-isolated serving requirement.

The full CMake suite still includes unrelated Swift/CBridge failures on the macOS/Ninja baseline;
those failures are outside the JS integration change. Phase 8 remains responsible for broader
functional coverage, strict TypeScript validation, browser execution, and final generated-output
smoke references.
