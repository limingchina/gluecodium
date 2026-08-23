# JavaScript Wrapper Cache and Ownership Contract

## Scope

Generated class and interface returns need a Gluecodium-owned cache because
Emscripten 6.0.6 does not canonicalize ordinary `std::shared_ptr` return
wrappers. This document defines the contract; implementation is gated on a
supported JavaScript lifecycle integration. A native-only C++ cache is not
sufficient.

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
The implementation must therefore either intercept explicit deletion and the
finalization path, or make explicit disposal a strict requirement and provide a
supported eviction operation.

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
	overrides or wraps `.delete()`, evicts the cache entry, and coordinates
	finalization.
2. An explicitly version-pinned embind integration that exposes equivalent
	wrapper lookup and lifecycle hooks, with a focused compatibility test for
	every supported Emscripten version.

Private embind internals such as `registeredInstances`, `ClassHandle.$$`, and
`RegisteredPointer_fromWireType` are not a supported boundary by themselves.