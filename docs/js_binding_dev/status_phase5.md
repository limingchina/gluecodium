# JavaScript/Embind Generator - Phase 5 Status

**Status**: In progress

## Item 1 - Referential Equality

**Status**: Partially implemented; native lifecycle integration remains deferred

**Commit**: `dab2bff75` - `Document embind referential equality limitation`

The first Phase 5 item tested whether a method returning the same
`std::shared_ptr` instance preserves JavaScript wrapper identity. The focused
harness probe added `Harness.self()` and asserted:

```js
assert.equal(harness.self(), harness);
```

The assertion failed under Emscripten 6.0.6. The same C++ pointer produced two
distinct JavaScript wrapper objects, even though the generated class uses an
embind `std::shared_ptr` holder.

Emscripten consults its internal `registeredInstances` table during pointer
conversion, but ordinary smart-pointer return handles are not inserted into
that table. Its built-in `FinalizationRegistry` provides leak-reduction cleanup
but does not provide referential equality.

The failed probe was removed from the stable Phase 4 harness. The full Phase 4
generation, Emscripten build, and Node.js regression harness still passes.

The complete finding is recorded in
`docs/js_binding_dev/spikes/referential_equality_spike.md`. A Gluecodium-owned
pointer-to-JavaScript-wrapper cache is required if the existing cross-language
pointer-equality contract is required for JavaScript. That cache must define
ownership, `.delete()` invalidation, raw-pointer and smart-pointer behavior,
explicit upcasts, and pthread safety.

The cache was not added as a C++ map of `emscripten::val`. Such a map is not a
complete implementation: the strong cached value keeps the JavaScript wrapper
reachable, while embind's public API provides no hook for generated code to
observe `.delete()` and evict that entry immediately. Checking `isDeleted()` on
a later lookup would leave stale entries retained and would not define safe
single-disposal behavior for aliases. Converting generated `std::shared_ptr`
returns to raw pointers would also lose the holder's ownership and deletion
semantics, so it is not an acceptable workaround.

The required contract is recorded in
`docs/js_binding_dev/wrapper_cache_design.md`. The generated JavaScript wrapper
layer is the preferred single integration point for canonical wrapper lookup,
`.delete()` eviction, `[Symbol.dispose]`, and optional finalization. An
explicitly version-pinned embind integration is the alternative. The contract
covers same-thread shared-pointer identity only; raw pointers, cross-type
upcasts, JS-implemented interface wrappers, and pthread marshalling remain
separate items.

The planned flow is that embind first creates a candidate handle for a
shared-pointer return. The generated layer checks the
`(native pointee address, exposed embind type)` key, reuses the live canonical
wrapper when present, and releases any duplicate candidate without creating a
second consumer-visible disposal obligation. The canonical wrapper's
`.delete()` evicts the cache entry, marks the wrapper disposed, and delegates
to embind exactly once; `[Symbol.dispose]()` uses that same path. The generated
layer owns JavaScript bookkeeping, not a second native owner: embind retains
the `std::shared_ptr` holder. Finalization must use the same path and remains
thread-gated for pthread builds.

The first implementation slice now emits `js/WrapperRuntime.mjs`. Consumers
apply `wrapModule(await createModule())` to the Emscripten module factory result.
The runtime patches only generated class/interface exports, uses public embind
`isAliasOf()`/`isDeleted()` APIs, and leaves enums and value types untouched.
Its cache holds weak references so live wrappers can be canonicalized without
preventing collection. The optional generated `FinalizationRegistry` evicts
cache metadata only; it never calls `.delete()` or accesses `emscripten::val`.
Embind's own finalization remains responsible for native-holder cleanup, which
keeps this generated callback outside the pthread thread-affinity hazard.

## Verification

The stable regression harness passes:

```text
Phase 4 harness OK
```

The failed identity assertion is retained as the original spike result. The
generated `WrapperRuntime.mjs` now provides the supported JavaScript-side
integration point for same-type, same-thread shared-pointer returns. The
runtime harness verifies same-object retrieval, explicit cache eviction through
`.delete()`, and `[Symbol.dispose]`. Native cleanup through a generated
finalizer remains deferred because the public embind API does not expose a safe
hook; embind's own finalization remains responsible for native-holder cleanup.

## Item 2 - Multiple Inheritance

**Status**: Verified

**Commit**: `abe50017c` - `Add JavaScript multiple inheritance bindings`

The generator now selects one primary embind `base<>` parent, preferring an open
class over a narrow interface, and flattens members from secondary parents onto
the derived registration. Flattened methods use an explicit derived-class
lambda because embind does not expose an inherited secondary-base member pointer
on the derived JavaScript prototype. Interfaces also register their
`std::shared_ptr` holders so interface-returning factory methods and explicit
upcasts resolve correctly.

The persistent harness covers:

- primary-base method and property access;
- flattened secondary-interface method and property access;
- factory returns typed as the secondary interface; and
- explicit `MultiClass` to `NarrowInterface` upcasting.

The complete generation, Emscripten build, and Node.js assertions pass:

```text
Phase 5 harness OK
```

The repository regression suite also passes:

```text
./gradlew test -q
```

The status update is recorded in commit `2555ad2ec` - `Record Phase 5 multiple
inheritance status`.

## Item 3 - JavaScript-Implemented Interfaces

**Status**: Verified

The JS generator now emits an `emscripten::wrapper<T>` trampoline for each
interface. Interface methods forward to the JavaScript implementation using
their generated JS names, and interface registrations mark methods as
`pure_virtual()` and expose the smart-pointer `allow_subclass` overload. This
enables `Interface.implement({...})` objects to be passed to native APIs that
accept `std::shared_ptr<Interface>`.

The persistent harness adds `JsCallback`, whose native implementation invokes
the callback through `MultipleInheritanceFactory.invokeJsCallback()`. The Node
assertion creates the implementation with `JsCallback.implement({...})`,
verifies the native-to-JavaScript-to-native return value, and explicitly
deletes the callback wrapper.

Verification passes:

```text
./gradlew :gluecodium:compileKotlin -q
Phase 5 harness OK
```

## Item 4 - JavaScript Callables (`LimeLambda`)

**Status**: Verified for synchronous single-threaded invocation

`LimeLambda` parameters are adapted from `emscripten::val` to native
`std::function` values. The generated adapter captures the JavaScript callable
and invokes its `call` method with the generated native argument and return
types. The persistent harness passes a JavaScript `String -> String` callable to
native code and verifies the returned value.

The callback is invoked synchronously on the WebAssembly thread that calls the
native method. This item does not claim cross-thread `emscripten::val` safety;
pthread behavior remains a separate Phase 5 item.

Verification passes:

```text
./gradlew :gluecodium:compileKotlin -q
Phase 5 harness OK
```

## Item 5 - Exceptions and `Return<T, Error>`

**Status**: Verified for enum-based and struct-backed errors

Methods declared with `throws` retain their generated C++
`Return<T, Error>` signature and are registered through an `emscripten::val`
adapter. Successful calls return an object with a `value` property; failed
calls return an object with an `error` property. Enum-based errors are exposed
as their numeric `std::error_code::value()`.

The persistent harness verifies both branches of synchronous `String throws
Callback` and `Void throws Callback` methods, plus success and payload-error
branches of `String throws CallbackWithPayload`. Struct-backed errors are
returned as their bound payload object under the `error` property.

Verification passes:

```text
./gradlew :gluecodium:compileKotlin -q
Phase 5 harness OK
```

## Item 6 - Pthreads and Cross-Thread `emscripten::val`

**Status**: Verified limitation; marshalling design deferred

The standalone spike in
`docs/js_binding_dev/spikes/pthreads_callbacks_spike/README.md` compiles with
Emscripten 6.0.6 and invokes a JavaScript callable from a native `std::thread`.
The runtime aborts with `val accessed from wrong thread`, confirming that a
stored `emscripten::val` cannot be moved to an arbitrary pthread. Generated
callbacks and `LimeLambda` adapters therefore guarantee synchronous invocation
on the owning WebAssembly thread only. `PROXY_TO_PTHREAD=1` remains a separate
application-module deployment concern because the embind-only probe has no
`main()` entry point.

The browser/COOP/COEP pass in the same spike directory (`serve.mjs`,
`test.html`, `browser-test.mjs` with headless Chromium) reproduces the
identical `val accessed from wrong thread` assertion under real cross-origin
isolation, confirming the constraint in both required target environments. A
thread-aware marshalling design remains future work; this item records the
constraint rather than claiming cross-thread support.

## Remaining Phase 5 Items

1. Design thread-aware callback marshalling for the pthread build.
2. Complete the generated JavaScript wrapper layer's native lifecycle
   integration after a supported embind deletion/finalization hook is available.
   The current runtime already combines the documented wrapper identity cache,
   `.delete()`/[Symbol.dispose] lifecycle, and thread-gated finalization policy.
3. Extend collection adapters to nested and nullable `Set`/container cases, or
   replace the inline adapters with a composable caster design.

Each item should be independently verified and committed before the next item
begins.