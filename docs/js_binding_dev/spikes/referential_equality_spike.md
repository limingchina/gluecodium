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

Phase 5 needs a Gluecodium-owned wrapper cache if the existing pointer-equality
contract is required for JavaScript. The supported contract is:

- identity key `(native pointee address, exposed embind type)`;
- one canonical wrapper per key on one WebAssembly thread;
- embind's existing `std::shared_ptr` holder remains the sole native owner;
- aliases do not create additional disposal obligations;
- `.delete()` evicts the canonical entry before releasing the embind holder;
- finalization either evicts the entry through the same lifecycle hook or is
    disabled by the contract in favor of required explicit disposal;
- deleted wrappers are never revived, including after pointer-address reuse;
- raw pointers and JS-implemented interface wrappers use separate policies;
- primary/upcast views are different keys unless explicit cross-type identity is
    implemented; and
- access is thread-local or marshalled to the owning WebAssembly thread.

A native-only `unordered_map<void*, emscripten::val>` does not satisfy this
contract. The strong `val` keeps the wrapper reachable, and Emscripten 6.0.6
does not expose a public hook for generated code to intercept embind's
`.delete()` and remove the cache entry. The implementation is therefore gated
on a generated JavaScript layer that owns wrapper creation and delete eviction,
or on an explicitly version-pinned embind lifecycle integration. The detailed
contract is recorded in `docs/js_binding_dev/wrapper_cache_design.md`.

This spike deliberately does not add an ad hoc cache. The stable Phase 4
harness remains focused on type mapping and explicit deletion. A same-object
assertion belongs in the harness only after the lifecycle integration exists.