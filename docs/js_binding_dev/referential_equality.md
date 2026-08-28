# JavaScript Referential Equality with Embind

## The Limitation

Referential equality has two parts at the language boundary:

1. Native pointer identity: two values refer to the same C++ object.
2. JavaScript object identity: two values are the same JavaScript object, so
   `===` is true.

These are not automatically the same thing in embind.

Consider this LimeIDL class:

```lime
class Harness {
    constructor create(seed: Int)
    fun self(): Harness
}
```

The native implementation returns the same shared pointer held by the
receiver:

```cpp
std::shared_ptr<Harness> Harness::self() {
    return shared_from_this();
}
```

The two native results refer to one object:

```text
harness  ------+
               +----> C++ Harness at 0x1234
self() result -+
```

However, ordinary embind smart-pointer conversion can create two JavaScript
handles:

```js
const harness = Harness.create(10);
const returned = harness.self();

harness === returned;                 // false without the Gluecodium runtime
harness.isAliasOf(returned);          // true
```

This affects normal JavaScript data structures as well:

```js
const values = new Map();
values.set(harness, "known");

values.get(returned);                  // undefined without canonicalization
```

The two wrappers can describe the same native object while still behaving as
different keys in a `Map`, different members of a `Set`, or different values
under `===`.

## Why Embind Does This

Embind wraps a native pointer and its holder in a JavaScript object. When a
method returns a `std::shared_ptr<T>`, the return conversion has to create a
JavaScript handle for that result. Emscripten 6.0.6 uses internal instance
tracking for some conversions, but ordinary smart-pointer return handles are
not reliably inserted into that table for canonical lookup.

Emscripten's built-in `FinalizationRegistry` addresses a different problem. It
helps detect or release leaked embind handles; it does not promise:

```text
same native pointer -> same JavaScript object
```

Converting the return to a raw pointer is not a valid workaround. It would
change the ownership and deletion behavior supplied by the `std::shared_ptr`
holder.

## The Gluecodium Solution

The generated JavaScript layer emits `js/WrapperRuntime.mjs`. Consumers apply
it after creating the Emscripten module:

```js
import createModule from "./module.mjs";
import { wrapModule } from "./WrapperRuntime.mjs";

const Module = wrapModule(await createModule());
```

For generated class and interface exports, the runtime canonicalizes handles
returned by methods, properties, and static functions:

```text
embind creates a candidate handle
              |
              v
generated runtime checks type and alias
        +-----+-----+
        |           |
  live alias     no alias
        |           |
delete candidate  cache candidate
return canonical  return candidate
```

The lookup uses the native alias relationship and the exposed embind type. A
live wrapper for the same native object and same exposed type is returned to
the caller. A duplicate candidate is deleted immediately, so it does not
create another JavaScript disposal obligation.

With the runtime applied, the example becomes:

```js
const harness = Harness.create(10);
const returned = harness.self();

assert.strictEqual(harness, returned);
assert.equal(harness.isAliasOf(returned), true);

harness.delete();
```

The current Phase 5 harness verifies this behavior and verifies that a new
wrapper is created after the canonical wrapper is deleted:

```js
assert.strictEqual(harness.self(), harness);

harness[Symbol.dispose]();
const freshHarness = Harness.create(10);
assert.notStrictEqual(freshHarness, harness);
```

## Ownership and Disposal

The cache does not create a second native owner. Embind's smart-pointer holder
remains responsible for the native ownership associated with the canonical
wrapper.

The generated runtime removes the canonical entry before delegating explicit
`.delete()` to embind. `[Symbol.dispose]()` uses the same path. A deleted
wrapper is never returned from a later lookup, and pointer-address reuse must
produce a fresh wrapper.

The cache uses weak references so it does not keep otherwise unreachable
JavaScript wrappers alive. Its optional `FinalizationRegistry` only removes
cache metadata. It does not call `.delete()` or access `emscripten::val`; embind
continues to own native finalization.

## Supported Boundary

The current guarantee is deliberately narrow:

```text
same native pointee
+ same exposed embind type
+ same WebAssembly thread
```

Identity is not promised across:

- `MultiClass` and `NarrowInterface` views created by an explicit upcast;
- raw-pointer returns, which need a separate ownership policy;
- JavaScript-implemented interface wrappers passed into native code; or
- pthread transfers and other cross-thread wrapper marshalling.

For example, two exposed types can refer to one native allocation without
being the same JavaScript object:

```js
const object = MultipleInheritanceFactory.getMultiClass();
const view = MultipleInheritanceFactory.upcastToNarrow(object);

object === view; // not guaranteed: the exposed embind types differ
```

The original Emscripten 6.0.6 experiment is recorded in
[spikes/referential_equality_spike.md](spikes/referential_equality_spike.md).
The complete cache and ownership contract is recorded in
[wrapper_cache_design.md](wrapper_cache_design.md).