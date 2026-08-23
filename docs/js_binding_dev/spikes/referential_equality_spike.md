# Spike: Referential Equality for Shared-Pointer Returns

## Result

**Status**: Fails with the current generated embind bindings

The Phase 5 harness added a `Harness.self()` method that returned the same
`std::shared_ptr<Harness>` instance held by the receiver. The JavaScript check

```js
assert.equal(harness.self(), harness);
```

failed because embind returned two distinct JavaScript wrapper objects for the
same C++ pointer.

The generated registration was:

```cpp
class_<::phase4::Harness>("Harness")
    .smart_ptr<std::shared_ptr<::phase4::Harness>>("Harness")
```

No custom generator code or explicit upcast was involved in this result.

## Toolchain Behavior

Emscripten 6.0.6 exposes `registeredInstances` and consults it from
`RegisteredPointer_fromWireType`, but ordinary smart-pointer return handles are
not inserted into that cache. Each return therefore creates a new JS handle.
Emscripten's built-in `FinalizationRegistry` still tracks smart-pointer handles
as a leak-reduction safety net, but it does not provide referential equality.

The existing multiple-inheritance spike remains valid for primary-base
registration, flattened secondary members, and explicit upcast calls. Its
referential-equality claim is limited to distinct C++ objects producing
distinct wrappers; same-object retrieval was not previously tested.

## Design Consequence

Phase 5 needs a Gluecodium-owned C++ pointer-to-JS-wrapper cache if the existing
pointer-equality contract is required for JavaScript. The cache must define:

- ownership and invalidation when `.delete()` is called;
- behavior for raw-pointer and `std::shared_ptr` returns;
- handling across primary-base and explicit upcast paths; and
- thread safety before pthreads support is added.

This spike deliberately does not add an ad hoc cache. The stable Phase 4
harness remains focused on type mapping and explicit deletion, while the cache
design and implementation are the next Phase 5 identity item.