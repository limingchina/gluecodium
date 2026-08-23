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

## Result

The probe compiles successfully but aborts on the current Emscripten/Node
configuration with `val accessed from wrong thread`: `emscripten::val` is
thread-affine, so generated callbacks and `LimeLambda` values must be invoked
on the thread that owns the handle. A future threaded design must marshal work
to the owning runtime thread instead of moving a stored `emscripten::val` into
an arbitrary pthread.

`PROXY_TO_PTHREAD=1` is a separate module-level option for applications with a
`main()` entry point. This embind-only probe has no `main()`, so it uses
`-pthread` and a worker pool directly to exercise the same thread-affinity
assertion.

The generated Phase 5 callback and lambda adapters therefore claim synchronous
same-thread invocation only. This spike does not establish browser behavior;
the browser pass still requires a COOP/COEP-enabled test page.