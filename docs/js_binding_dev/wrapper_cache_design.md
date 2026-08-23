# JavaScript Wrapper Cache and Ownership Contract

## Scope

Generated class and interface returns use a Gluecodium-owned cache because
Emscripten 6.0.6 does not canonicalize ordinary `std::shared_ptr` return
wrappers. This document defines the implemented generated JavaScript wrapper
layer, which is also the lifecycle integration
point for `.delete()`, `[Symbol.dispose]`, and any `FinalizationRegistry`
safety net. A native-only C++ cache is not sufficient.

The first implementation slice is emitted as `js/WrapperRuntime.mjs`. A
consumer applies it to the Emscripten module factory result:

```js
import createModule from "./module.mjs";
import { wrapModule } from "./WrapperRuntime.mjs";

const Module = wrapModule(await createModule());
```

The runtime patches only generated class and interface exports. Enums,
structs, and other value exports remain untouched.

## Identity

The cache key is the pair `(native pointee address, exposed C++ type)`. A live
return of the same pointer through the same exposed type returns the same
JavaScript object. Different exposed types, such as `MultiClass` and
`NarrowInterface`, have different prototypes and therefore may produce
different wrappers even when they refer to the same native object. The cache
does not promise identity across an explicit upcast boundary.

## Ownership and disposal

The cache must not create a second native owner. The first conversion creates
the normal embind smart-pointer wrapper; subsequent returns reuse that wrapper.
The canonical wrapper owns the embind holder, and aliases do not create extra
`.delete()` obligations. JavaScript callers must call `.delete()` exactly once
for each canonical wrapper they receive.

`.delete()` must evict the cache entry before releasing the embind holder. A
later lookup must never return a deleted wrapper, and pointer-address reuse must
create a fresh wrapper. Checking `isDeleted()` only during a later lookup is a
fallback sanity check, not a lifecycle implementation: a strong cached handle
would keep the wrapper reachable indefinitely and prevent normal finalization.
The generated layer intercepts explicit deletion and provides the supported
eviction operation. Native garbage-collection finalization remains embind's
responsibility because the public API does not expose a callback hook for the
generated layer to invoke native deletion safely.

## Generated Wrapper Responsibilities

The generated JavaScript layer sits between the raw embind handle and
the consumer. A shared-pointer return first produces an embind candidate
handle. The generated layer then looks up the `(native pointee address,
exposed embind type)` key. It returns the live canonical wrapper when one
exists and disposes the duplicate candidate without creating another
consumer-visible `.delete()` obligation. Otherwise, it records the candidate
as the canonical wrapper and returns the generated wrapper object.

The generated wrapper's `.delete()` is the single explicit disposal path. It
evicts the cache entry, marks the wrapper disposed, and delegates release of
the underlying embind handle exactly once. `[Symbol.dispose]()` invokes the
same path rather than implementing separate ownership logic. The wrapper layer
owns JavaScript cache bookkeeping; embind's smart-pointer holder remains the
sole native owner held for that JavaScript wrapper.

Any `FinalizationRegistry` integration must track the generated wrapper and use
the same eviction path. It is a best-effort fallback, never an additional
owner, and must be disabled or marshalled when the finalizer may run on a
different thread from the wrapper's owning WebAssembly runtime.

In the current implementation, the generated registry only evicts weak cache
metadata. It does not call `.delete()` or access `emscripten::val`; embind's
own finalization mechanism remains responsible for releasing the native holder
when the embind wrapper becomes unreachable. This keeps the generated callback
outside the thread-affine native API. The generated registry is opt-in through
`wrapModule(module, { enableFinalization: true })`; it evicts cache metadata
only and does not replace embind's native finalizer.

## Threads

`emscripten::val` is thread-affine. The cache is therefore `thread_local`, not
process-global. Identity is guaranteed only when a pointer is returned on the
same WebAssembly thread. Cross-thread callback and wrapper marshalling remain
blocked by the pthread finding documented in
`spikes/pthreads_callbacks_spike/README.md`.

The cache is deliberately limited to same-thread shared-pointer returns.
Raw-pointer returns, JS-implemented interface handles passed into native code,
and cross-type upcasts require separate ownership and marshalling rules before
they can claim referential equality.

## Integration Gate

The implementation must use one of these supported boundaries:

1. A generated JavaScript wrapper layer that owns canonical wrapper creation,
  overrides or wraps `.delete()`, exposes `[Symbol.dispose]` as its alias,
  evicts the cache entry, and coordinates optional finalization on the owning
  WebAssembly thread.
2. An explicitly version-pinned embind integration that exposes equivalent
  wrapper lookup and lifecycle hooks, with a focused compatibility test for
  every supported Emscripten version. If this boundary is used, the same
  integration must define the disposal alias and finalizer thread policy.

Private embind internals such as `registeredInstances`, `ClassHandle.$$`, and
`RegisteredPointer_fromWireType` are not a supported boundary by themselves.

## Finalization and Pthreads

Explicit `.delete()` and `[Symbol.dispose]` are safe deterministic APIs when
called by the consumer on the owning runtime thread. `FinalizationRegistry`
cleanup is not enabled by default for pthread builds until cross-thread
marshalling is implemented and verified. The pthread spike demonstrated that
calling `emscripten::val` from the wrong thread aborts the runtime, so a
finalizer must not assume that its JavaScript callback runs on the WebAssembly
thread that owns the wrapper.