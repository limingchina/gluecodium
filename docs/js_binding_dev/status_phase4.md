# JavaScript/Embind Generator - Phase 4 Status

**Status**: Complete

**Commit**: `45ce577fe` - `Expand Phase 4 JavaScript embind coverage`

## Scope Delivered

Phase 4 establishes the first end-to-end type-mapping slice for the JavaScript/WebAssembly
generator. The generated embind C++ now covers:

- Nullable scalar parameters and return values, including `null` and `undefined` handling.
- `List<T>` parameters and return values through JavaScript arrays and `register_vector<T>`.
- `Map<K, V>` parameters and return values through JavaScript `Map` objects and explicit entry
  conversion. Native `std::unordered_map` is kept out of embind's incompatible `register_map`
  path.
- Structs through embind `value_object` registrations and object-literal construction.
- Enums through fully qualified C++ enumerator expressions, for example
  `::phase4::Mode::ON`.
- 64-bit integers as JavaScript `bigint`, requiring `-sWASM_BIGINT=1`.
- Shared-pointer class bindings and explicit `.delete()` lifecycle handling.

The generator also emits optional and vector registrations with qualified C++ names, preserves
the TypeScript declaration stubs, and uses explicit adapters where direct embind conversion is
not reliable with the target Emscripten version.

## Persistent Harness

The development harness in `docs/js_binding_dev/harness/` runs the complete loop:

1. Generate C++ and JavaScript bindings from `Phase4Harness.lime`.
2. Configure and build the generated sources with `emcmake` and Ninja.
3. Execute the resulting Wasm module with Node.js.

The fixture validates static and instance methods, properties, nullable values, vectors, maps,
struct round trips, enum round trips, 64-bit values beyond the JavaScript safe-integer range,
and explicit object deletion.

## Verification

The following checks passed:

```text
Phase 4 harness OK
./gradlew test -q
JsGenerator.kt diagnostics: no errors
```

The harness was validated with Emscripten 6.0.6, Node.js 23.6.1, CMake 4.3.1, and Ninja.

## Known Warnings and Limits

- The harness Lime fixture produces existing documentation warnings for undocumented properties,
  parameters, and return values.
- CMake 4.3.1 reports the known Emscripten shared-library compatibility warning; the harness
  still configures, builds, links, and runs successfully.
- Direct `std::optional<T>` embind registration remains avoided because it is not reliable with
  the target Emscripten version; nullable values use generated `emscripten::val` adapters.
- Callback trampolines, JavaScript-implemented interfaces, referential-equality validation,
  multiple-inheritance validation, pthread behavior, and broader lifecycle design are Phase 5
  work and are not included in this commit.

## Phase 5 Handoff

Phase 5 should proceed one independently verifiable item at a time. Emscripten already provides
a `FinalizationRegistry` safety net for smart-pointer handles in the current toolchain, while
the generated TypeScript contract continues to require explicit `.delete()` calls. The next
Phase 5 work should validate lifecycle and referential-equality behavior in the persistent
harness before adding generator changes.