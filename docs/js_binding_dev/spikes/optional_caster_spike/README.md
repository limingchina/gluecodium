# Spike: `std::optional<T>` and `Return<T, E>` casters for embind

Date: 2026-08-22 · Emscripten: `emcc 6.0.6` (Homebrew) · Node: v23.6.1

## Question

Does embind support `std::optional<T>` natively, or does Gluecodium need to generate a custom
type caster? How should `Return<T, E>` be exposed? Do `register_vector` / `register_map` work
as assumed in the plan?

## Findings

### 1. Native `std::optional<T>` support exists — but requires explicit registration

Emscripten ≥ some 3.x/4.x version ships a built-in caster in
`sysroot/include/emscripten/val.h`:

```cpp
template <typename T>
struct BindingType<std::optional<T>> { ... }   // maps nullopt -> JS undefined
```

However it is **not auto-registered**. Calling a function whose signature contains
`std::optional<int>` without prior registration fails at runtime with:

```
UnboundTypeError: Cannot call getOpt due to unbound types: NSt3__28optionalIiEE
```

(`spike.cpp`, `spike2.cpp` reproduce the failure; the built-in caster also means we must NOT
define our own specialization — it would be a redefinition compile error.)

The fix is one generated line per distinct instantiation (`spike3.cpp`):

```cpp
register_optional<int>();          // inside EMSCRIPTEN_BINDINGS
```

Result: `getOpt(true) === 42`, `getOpt(false) === undefined`. ✔

**JS-side contract caveat:** absent values are `undefined`, **not** `null`.
Passing `null` for an `std::optional<int>` parameter throws
`TypeError: Cannot convert "null" to int`. The `.d.ts` stubs should therefore declare
optional parameters as `T | undefined` and document that `null` is rejected.

### 2. `Return<T, E>` via value_object with optional fields works

Gluecodium's `Return<T,E>` is a struct of two optionals. Binding it as a `value_object`
with both optional fields works out of the box once each element type's
`register_optional<T>()` has been emitted (`spike4.cpp`):

```
divide(6,3) = {"value":2}
divide(1,0) = {"error":"division by zero"}
```

Fields that are `nullopt` are simply omitted from the returned JS object.

### 3. `register_vector<T>` / `register_map<K,V>` confirmed

`spike5.cpp`: `register_vector<int>("VectorInt")` + `register_map<std::string,int>(...)`
work as planned; returned containers expose `size()`/`get(i)` rather than being plain JS
arrays/maps. This matches plan §4.2 — the generator must collect distinct instantiations.

## Decision for Phase 4

1. **No custom casters needed.** Use embind's built-in `std::optional` support.
2. Generator emits `register_optional<T>()` for every distinct `Optional<T>` instantiation,
   analogous to the `register_vector`/`register_map` collection pass.
3. TS stubs use `T | undefined` spelling for optional types (not `T | null`) — update
   `JsNameResolver` accordingly.
4. `Return<T,E>` needs no special handling beyond (2): bind as value_object with two
   optional fields.
5. Vector/map results are embind class instances (not native JS arrays); document this in
   the stubs' doc comments; ergonomic conversion can be revisited later if needed.

## Files

- `spike.cpp` — reproduces UnboundTypeError without registration
- `spike2.cpp` — documents that a custom specialization conflicts with the built-in one
- `spike3.cpp` — solution: `register_optional<T>()`; also shows `null` rejection
- `spike4.cpp` — `Return<T,E>` pattern via value_object with optional fields
- `spike5.cpp` — `register_vector` / `register_map`
