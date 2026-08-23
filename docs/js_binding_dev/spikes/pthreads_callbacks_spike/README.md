# Emscripten Pthreads Callback Spike

This spike checks whether a JavaScript callable held as an `emscripten::val`
can be invoked from a native `std::thread`. It is intentionally independent of
the generated bindings so that the threading behavior is isolated from
Gluecodium templates.

Build and run it from this directory with Emscripten 6.0.6:

```sh
em++ spike.cpp -std=c++17 -pthread \
    -lembind -fexceptions \
    -sPTHREAD_POOL_SIZE=1 \
    -sMODULARIZE=1 -sEXPORT_ES6=1 -sWASM_BIGINT=1 \
    -sALLOW_MEMORY_GROWTH=1 \
    -o pthreads_callbacks_spike.mjs
node test.mjs 2>&1 | tee /tmp/pthreads_callbacks_spike.log
grep -q "val accessed from wrong thread" /tmp/pthreads_callbacks_spike.log
```

The JavaScript function is created on the module's JavaScript side and passed
to native code. Native code captures the `emscripten::val`, invokes it on a
worker thread, joins that thread, and reports either the returned string or
the exception text.

## Browser pass

The same probe runs in a browser under real COOP/COEP headers, as required by
the Q3 decision in `docs/js_binding_dev/js_binding_plan.md`. The browser build
uses the same flags as the Node build; the only difference is the environment:

```sh
em++ spike.cpp -std=c++17 -pthread \
    -lembind -fexceptions \
    -sPTHREAD_POOL_SIZE=1 \
    -sMODULARIZE=1 -sEXPORT_ES6=1 -sWASM_BIGINT=1 \
    -sALLOW_MEMORY_GROWTH=1 \
    -o pthreads_callbacks_spike.mjs
```

`serve.mjs` is a minimal static file server that adds
`Cross-Origin-Opener-Policy: same-origin` and
`Cross-Origin-Embedder-Policy: require-corp` so that `SharedArrayBuffer` is
available and the pthread pool can start. `test.html` loads the module, checks
`crossOriginIsolated`, and invokes the same cross-thread probe;
`browser-test.mjs` drives it with headless Chromium via Playwright:

```sh
npm install playwright && npx playwright install chromium
node serve.mjs 8080 &
node browser-test.mjs
kill %1
```

## Result

The probe compiles successfully but aborts on the current Emscripten/Node
configuration with `val accessed from wrong thread`: `emscripten::val` is
thread-affine, so generated callbacks and `LimeLambda` values must be invoked
on the thread that owns the handle. A future threaded design must marshal work
to the owning runtime thread instead of moving a stored `emscripten::val` into
an arbitrary pthread.

The browser pass reproduces the identical assertion under headless Chromium
with real COOP/COEP headers (`crossOriginIsolated === true`): the worker
pthread aborts with `pthread_equal(thread, pthread_self()) && "val accessed
from wrong thread"` from `emscripten/val.h`, surfacing as an uncaught
`RuntimeError` in the worker and an `unhandledrejection` on the main thread.
The thread-affinity constraint is therefore confirmed in both required target
environments (Node.js and browser), not just Node.js.

`PROXY_TO_PTHREAD=1` is a separate module-level option for applications with a
`main()` entry point. This embind-only probe has no `main()`, so it uses
`-pthread` and a worker pool directly to exercise the same thread-affinity
assertion.

The generated Phase 5 callback and lambda adapters therefore claim synchronous
same-thread invocation only. This spike does not establish behavior for a
`PROXY_TO_PTHREAD` deployment; a thread-aware marshalling design remains
future work.