# JavaScript/Embind Generator - Phase 5 Status

**Status**: In progress

## Item 1 - Referential Equality

**Status**: Verified limitation; implementation deferred

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

The cache was not added in this item. Emscripten 6.0.6 keeps the relevant
`registeredInstances` table internal to the embind runtime. Its supported
`registerInheritedInstance` API is reserved for `allow_subclass` wrappers and
is not exported to generated modules. Converting generated `std::shared_ptr`
returns to raw pointers would lose the holder's ownership and deletion
semantics, so it is not an acceptable workaround.

## Verification

The stable regression harness passes:

```text
Phase 4 harness OK
```

The failed identity assertion is intentionally retained as a documented spike
result. Referential equality remains an explicit JavaScript-target limitation
until a stable cache integration point is designed for the generated module.

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

## Remaining Phase 5 Items

1. Add pthread callback and cross-thread `emscripten::val` spike coverage.

Each item should be independently verified and committed before the next item
begins.