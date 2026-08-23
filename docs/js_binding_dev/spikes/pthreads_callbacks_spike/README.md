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
grep -q "PASS: callback marshalled to the runtime thread" /tmp/pthreads_callbacks_spike.log
```

The JavaScript function and Promise settlement callbacks are passed to native
code. Native code stores them in a short-lived state object, queues one
`emscripten_async_run_in_main_runtime_thread(EM_FUNC_SIG_VI, ...)` operation,
and destroys the state only after the runtime-thread operation settles the
Promise. The standalone module exposes `pumpRuntimeQueue()` because it has no
application event loop that would otherwise drain the runtime queue.

The callback adapter returns a tagged result object:

```js
{ ok: true, value }
{ ok: false, error }
```

The adapter catches JavaScript exceptions and converts them to the second
form before calling native code. This is required because an arbitrary
JavaScript `Error` thrown by `emscripten::val::call` is rethrown by generated
Embind glue rather than caught by a native C++ `try`/`catch` in this
configuration. Native exceptions are still converted to rejection strings by
the runtime-thread function.

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

The original direct worker invocation aborts with `val accessed from wrong
thread`: `emscripten::val` is thread-affine, so generated callbacks and
`LimeLambda` values must not be invoked from an arbitrary pthread. The
implemented design marshals the invocation to the owning runtime thread and
settles the Promise there. Node.js verifies both the successful callback path
and a JavaScript exception converted by the adapter into rejection data.

The browser pass succeeds under headless Chromium with real COOP/COEP headers
and `crossOriginIsolated === true`, verifying the same runtime queue hop with
an actual pthread-enabled browser module.

`PROXY_TO_PTHREAD=1` is a separate module-level option for applications with a
`main()` entry point. This embind-only probe has no `main()`, so it uses
`-pthread` and a worker pool directly to exercise the same thread-affinity
assertion.

The existing generated Phase 5 callback and lambda adapters still claim
synchronous same-thread invocation only. The spike establishes the reusable
dispatch design for a future asynchronous callback surface; it does not change
existing synchronous APIs or claim that native C++ can catch arbitrary
JavaScript exceptions. A generated async adapter must provide the tagged-result
conversion at the JavaScript boundary and must arrange for the runtime queue to
be pumped by the host/application.