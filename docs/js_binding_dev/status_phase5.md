# JavaScript/Embind Generator - Phase 5 Status

**Status**: In progress

## Item 1 - Referential Equality

**Status**: Investigated; implementation remains open

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

## Verification

The stable regression harness passes:

```text
Phase 4 harness OK
```

The failed identity assertion is intentionally retained as a documented spike
result rather than a passing production test until the cache design is defined.

## Item 2 - Multiple Inheritance

**Status**: Verified

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

## Remaining Phase 5 Items

1. Design and implement the pointer-to-wrapper cache for same-object identity.
2. Add JavaScript-implemented interface and callback trampoline coverage.
3. Add callable `LimeLambda` coverage and document callback thread behavior.
4. Add exception and `Return<T, Error>` behavior where it belongs in the
   generator/build plan.
5. Add pthread callback and cross-thread `emscripten::val` spike coverage.

Each item should be independently verified and committed before the next item
begins.