# JavaScript/Embind Generator - Phase 8 Status

**Status**: In progress; Strings, BuiltinTypes, and Enums Node.js functional coverage is passing

**Date**: 2026-08-23

## Checkpoint Scope

The first Phase 8 checkpoint adds a Node.js functional-test harness modeled on the Python
functional tests in the parallel `gluecodium1` checkout. It now enables three feature groups for
the `js` generator:

- `Strings`: string parameters and returns, C-string conversion, overloaded static methods, and
  read-only static properties;
- `BuiltinTypes`: Boolean, Float, Double, signed and unsigned integer mappings, including 64-bit
  values as JavaScript `bigint`.
- `Enums`: enum member export and round-trip behavior, including enums used by type collections.

The harness uses Node's built-in `node:test` runner and CTest. CMake copies the test modules into
the build tree and passes the generated Emscripten module through `GLUECODIUM_JS_MODULE`.

## Verification

With Emscripten and Node.js available:

```bash
rm -rf build-functional-js
export GLUECODIUM_PATH="$PWD"
emcmake cmake -S functional-tests -B build-functional-js -G Ninja \
  -DGLUECODIUM_GENERATORS_DEFAULT='cpp;js' \
  -DFUNCTIONAL_BUILD_JS_TESTS=ON
cmake --build build-functional-js --target functional_bindings_js
ctest --test-dir build-functional-js --output-on-failure -R unit_tests_javascript
```

The build and filtered CTest run pass for the checkpoint scope. The generated module is compiled
with `-sWASM_BIGINT=1`, and the Node tests assert `bigint` values for `Long` and `ULong` methods.

## Generator Fixes Exercised

The first tests found several embind generation defects that are fixed in this checkpoint:

- read-only instance properties emit getter-only `.property` registrations, while read-only
  static properties use a named getter function because embind has no function-based
  `.class_property` overload;
- overloaded functions use the typed adapter path so their C++ overload is resolved at generation
  output compile time.
- generated struct field pointers use C++ name resolution, preserving native names such as
  `set_field` when the JavaScript name is `setField`;
- enum bindings avoid Emscripten runtime names such as `InternalError` by using a distinct embind
  public name while retaining the generated C++ type identity.

## Next Work

`Structs` has an initial Node test file present in the worktree for the next modular iteration,
but is intentionally not included or enabled in this checkpoint. Its broader model currently
causes JS generation to fail before compilation. The Node versions tested locally
(22.13.1, 22.19.0, 23.6.1, 24.16.0, and 25.7.0) all treat a directory argument to `node --test`
as a module entry rather than a test collection, so the harness passes explicit test-file paths.
The next iteration should first fix the expanded-model generator failure, then enable enum and
value-object tests one feature group at a time.