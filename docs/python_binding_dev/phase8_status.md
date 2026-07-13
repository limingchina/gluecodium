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
- **8.2 Functional tests (pytest)** — ⚠️ BLOCKED on generator correctness.

## What works

The Python generator now **generates, compiles, and links** a complete pybind11
extension module (`functional.cpython-314-darwin.so`) for the functional Lime set.
All pybind11 binding `.cpp` files compile cleanly once the feature set is narrowed
(see below). The CMake integration (parent `functional/CMakeLists.txt` + the
`functional/python/CMakeLists.txt` test driver) is in place and the build script
drives it end-to-end.

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
- `Dates`, `Durations` — date/duration binding gaps.
- `RefEquality` (in `Equatable`), `Comments`, `ComplexListeners`, `CppConst`,
  `CppNoexcept`, `Strings`, `Enums`, `FieldConstructors`, `Visibility`, `Interfaces`,
  `ListenersWithReturnValues`, `Locales`, `Nesting`, `NoCache`, `Structs`,
  `StructsInTypes`, `StructsImmutable`, `PlatformNames`, `Classes`,
  `InstanceInStruct`, `BuiltinTypes`, `StructsWithCompanion`, `UnderscorePackage`,
  `CrossPackageNameClash`, `TypeDefs`, `CallbacksWithThreads` — various
  constructor/arg-count, listener, enum, name-clash, and threading gaps.

Only **5 features remain enabled for `python`**: `Constants`, `CircularDependencies`,
`DeclarationOrder`, `EscapedNames`, `FullName`.

## Remaining blocker (8.2)

Even the simplest enabled feature (`Constants`) generates broken Python:

```python
# test/Constants.py
from test.DOUBLE_CONSTANT import DOUBLE_CONSTANT   # <-- submodule does not exist
from test.INT_CONSTANT import INT_CONSTANT
...
```

The generator emits each constant as a cross-module import instead of a module-level
variable. Root cause: `PythonImportsCollector` uses `collectValueImports = true`,
which turns constant-to-constant references into bogus imports. The submodules are
never generated, so `import test.Constants` fails and pytest cannot collect.

Additionally, the functional test files written in `functional/python/test/` assume
a `snake_case` module naming (e.g. `test.constants`), but the generator emits
`PascalCase` module names matching the Lime type (e.g. `test.Constants`). Every test
file's imports would need rewriting once the generator is fixed.

## Follow-up work (not in this phase)

1. Fix constant generation (module-level variables, not cross-module imports).
2. Fix the broader generator gaps listed above (overloads, trampolines, external
   types, collections, dates/durations, lambdas, properties, ref-equality,
   visibility, name-clashes, threading) and re-enable the features one by one.
3. Rewrite the functional pytest files to match the actual generated `PascalCase`
   module/class names, then run them green.
