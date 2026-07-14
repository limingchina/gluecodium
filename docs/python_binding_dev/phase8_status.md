# Phase 8: Testing — Status

**Date:** 2026-07-13
**Branch:** `python_bind`

## Summary

Phase 8 covers three sub-parts:

- **8.1 Smoke tests** — ✅ PASS (verified in prior session; regenerated reference
  output committed alongside the generator changes).
- **8.3 Functional test build script** — ✅ DONE. `functional-tests/scripts/build-python-functional`
  configures CMake with `GLUECODIUM_GENERATORS_DEFAULT="cpp;python"`, builds the
  pybind11 extension module, copies the generated wrapper package next to the `.so`,
  and runs pytest via ctest.
- **8.2 Functional tests (pytest)** — 🟡 PARTIAL. Phase A features A1-A7 are now
  enabled for Python and their generated binding translation units compile. The
  focused `Constants` pytest passes (6 tests), while the broader CTest run is
  blocked by the harness selecting Miniconda Python 3.12 and by an unrelated
  unresolved symbol when importing the aggregate extension.

## What works

The Python generator now generates the Phase A bindings and all A1-A7 pybind11
translation units compile cleanly. The aggregate extension is produced, but
importing it currently fails on the unrelated
`SomeOpenNumberWrapperClass::make(int)` symbol. The CMake integration (parent
`functional/CMakeLists.txt` + the
`functional/python/CMakeLists.txt` test driver) is in place and the build script
drives it end-to-end.

The completed Phase A commits include `ae8325438` (A4), `eb0899996` (A5),
`4b35efec8` (A6), and `16efce997` (A7), in addition to the earlier A1-A3 work.
The A7 fix corrected interface property getter trampolines that incorrectly
returned `std::string&` when the generated C++ interface returned `std::string`.

The `Constants` feature now generates correct Python (module-level constants, nested
enums, `True`/`False`/`float('nan')` literals) and its pytest passes:

```bash
cd functional-tests/build-python/functional/python
PYTHONPATH=".../build-python/functional" python3.14 -m pytest tests/constants_test.py
# 6 passed
```

## Generator bugs fixed during Phase 8

1. **`Return<T, Error>` type caster** (`Pybind11ReturnCaster.mustache`) — the
   `{{returnTypeFullName}}` variable was not passed, producing an empty
   `struct type_caster<::Return<...>>` that failed to compile. Now passed from
   `PythonGenerator` as `(internalNamespace + "Return").joinToString("::")`.
2. **`fullName` qualification crash** (`PythonGenerator.kt`) — `getFullyQualifiedName`
   was called for `LimeException` elements, which have no C++ name rule, throwing
   `IllegalArgumentException`. Now returns `""` for exceptions (they are excluded
   from the `using` alias by the `isException` predicate anyway).
3. **Duplicate `py::init<>()`** (`PythonGeneratorPredicates.kt`) — a struct with
   all-defaulted fields emitted both a default and an all-fields constructor.
   `needsAllFieldsConstructor` now returns `false` when a default constructor exists.
4. **Self-import** (`PythonGenerator.kt`) — types referencing themselves (e.g.
   `Greeter.create()` returns `Greeter`) emitted a circular `from ...Greeter import
   Greeter`. Filtered out in `generatePythonFile`.
5. **Constant generation** (`PythonImportResolver.kt`, `PythonNameResolver.kt`,
   templates) — constants were emitted as bogus cross-module imports
   (`from test.X import X`) and bare `NaN`/`true` literals. Fixed by:
   - `PythonImportResolver.resolveElementImports` now returns `emptyList()` for
     `LimeConstant` (constants are module-level variables, never imported).
   - `PythonImportResolver.resolveValueImports` returns `emptyList()` for
     `LimeValue.Constant` (constant-to-constant references resolve in place).
   - `PythonNameResolver.resolveValue` renders booleans as `True`/`False` and
     `LimeValue.Special` literals as `float('nan')`/`float('inf')`/`float('-inf')`.
   - Templates (`PythonClass`/`PythonStruct`/`PythonInterface`) emit nested
     enumerations and constants via `{{#enumerations}}`/`{{#constants}}`; new
     `PythonConstant.mustache` renders `NAME = value`.
   - `constants_test.py` imports from the generated `PascalCase` modules
     (`test.Constants`, `test.ConstantsSkipCpp`) and asserts the NaN/Infinity
     constants.

## Feature set narrowed (Option A)

To get a clean compile, `python` was removed from the `feature(...)` lists of the
following functional features (their Lime inputs exercise generator paths that are
not yet implemented for Python):

- `ExternalTypes`, `DartExternalTypes` — external-type binding gaps (cpp-name
  qualification, external member getters, type-collection `using` alias).
- `Inheritance`, `MultipleInheritance` — interface-inheritance trampoline does not
  override inherited pure-virtual methods (abstract-class instantiation failure).
- `Properties`, `MethodOverloading` — overload `def` resolution and trampoline
  virtual-override gaps.
- `Errors`, `Blob` — `Errors.lime` imports an external error enum from
  `ExternalTypes` (C++ impl not built when `ExternalTypes` is dropped); `Blobs.lime`
  imports `another.TypeCollectionWithEnums` from `Errors2.lime`.
- `GenericTypes`, `Lambdas`, `Defaults` — collection/array argument-count mismatches,
  lambda overloads, immutable-struct-with-defaults.
- `RefEquality` (in `Equatable`), `Comments`, `ComplexListeners`, `CppConst`,
  `CppNoexcept`, `FieldConstructors`, `Visibility`,
  `ListenersWithReturnValues`, `Locales`, `Nesting`, `NoCache`,
  `StructsInTypes`, `StructsImmutable`, `PlatformNames`,
  `InstanceInStruct`, `StructsWithCompanion`, `UnderscorePackage`,
  `CrossPackageNameClash`, `CallbacksWithThreads` — various
  constructor/arg-count, listener, enum, name-clash, and threading gaps.

The currently enabled Python features are `Strings`, `BuiltinTypes`, `Classes`,
`Interfaces`, `Structs`, `TypeDefs`, `Enums`, `CircularDependencies`, `Constants`,
`Dates`, `Durations`, `DeclarationOrder`, `EscapedNames`, and `FullName`.

## Remaining blocker (8.2)

The `Constants` feature is fixed and its pytest passes. A1-A7 are now enabled and
compile, but focused runtime tests that import the aggregate module remain blocked
by `SomeOpenNumberWrapperClass::make(int)`. The broader generator gaps (overloads,
inherited trampolines, external types, collections, lambdas, properties,
ref-equality, visibility, name clashes, and threading) still keep the remaining
functional features narrowed out. The CTest harness also uses Miniconda Python
3.12 instead of the CPython 3.14 runtime used to build the extension.

## Follow-up work (not in this phase)

1. ~~Fix constant generation (module-level variables, not cross-module imports).~~ ✅ DONE.
2. Fix the broader generator gaps listed above (overloads, trampolines, external
   types, collections, dates/durations, lambdas, properties, ref-equality,
   visibility, name-clashes, threading) and re-enable the features one by one.
3. Rewrite the remaining functional pytest files to match the actual generated
  `PascalCase` module/class names, then run them green as each feature is
  re-enabled. The A6 and A7 tests now use the generated names.
