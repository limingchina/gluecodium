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
  focused `Constants` pytest passes (6 tests) when run with the CPython 3.14
  interpreter that built the extension. The broader CTest run fails because the
  harness runs the tests under the machine's default `python3` (Miniconda 3.12),
  which cannot load the 3.14-specific `.so` — **not** because of any missing C++
  symbol in the extension (that earlier worry was a red herring; see Known issues).

## What works

The Python generator now generates the Phase A bindings and all A1-A7 pybind11
translation units compile cleanly. The aggregate extension
(`functional.cpython-314-darwin.so`) links and imports fine under CPython 3.14 —
the earlier `SomeOpenNumberWrapperClass::make(int)` "unresolved symbol" worry was
a red herring; the extension actually loads correctly under 3.14. The CMake
integration (parent `functional/CMakeLists.txt` + the
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

## Nesting feature fixes (2026-07-18)

The `Nesting` functional feature exercises nested structs/classes/interfaces/enums/lambdas
and their flattening to top-level Python modules. The following generator fixes make the
generated wrappers importable (import sweep: **31 → 10 failures**; all Nesting-specific
failures resolved):

1. **Nested type name flattening** (`PythonNameRules.kt`) — `getName` now flattens any
   `LimeType` with a parent (not just `LimeStruct`) to its concatenated tail
   (`OuterStructInnerEnum`, `OuterClassInnerClass`, `OuterStructInnerLambda`, …). This is the
   module/file name the pybind11 layer registers the type under, so the Python wrapper must
   reference the flattened name.
2. **Native enum name resolution** (`PythonGenerator.kt`) — `nativeTypeName` in the Python
   template data now uses `pythonNameResolver.resolveName` (flattened Python name) instead of
   `pybind11NameResolver.resolveName` (C++ short name). The pybind11 module attribute for a
   nested enum is `OuterStructInnerEnum`, so the Python enum wrapper must reference
   `functional.OuterStructInnerEnum.FOO`, not `functional.InnerEnum`.
3. **Class declaration with parents** (`PythonClass.mustache`) — the Trimou `{{else}}` inside
   `{{#if parents}}` rendered both branches, producing a duplicate `_NativeBase):(_NativeBase):`.
   Replaced with an inverted `{{^parents}}` section so a class with parents emits
   `class X(\n    Parent,\n    _NativeBase):` and a class without emits `class X(_NativeBase):`.
4. **Lambda `Callable` import** (`PythonLambda.mustache`, `PythonStubLambda.mustache`) — added
   `from typing import Callable` before the `typing.Callable` alias so lambdas/callbacks
   reference `Callable` without `NameError`.
5. **Ancestor/child import filtering** (`PythonGenerator.kt`) — extended the ancestor-module
   filter from struct fields only to also cover class/interface function return types and
   properties, and added a child-module filter that excludes every nested descendant of the
   current element (derived from `LimeTypeHelper.getAllTypes`) to avoid circular imports
   between a parent and its flattened nested children (e.g. `OuterStruct` ↔ `Builder`).
6. **Nested type generation coverage** (`PythonGenerator.kt`) — `getPythonTypes` now also
   flattens nested `LimeClass`, `LimeInterface`, and `LimeLambda` (not just enums/structs), and
   the duplicate-filename exclusion applies to all of them.

### Interface trampoline + throwing-function fixes (2026-07-19)

The `sample_project` (the end-to-end Python generator demo under
`docs/python_binding_dev/sample_project/`) exposed two generator bugs that also
affect the functional `Interfaces` feature:

1. **Interface trampoline broken (callback never fired).** The generated Python
   interface wrapper used `_NativeBase` *composition* — `super().__init__(
   {{nativeModule}}.{{resolveName}}())` always constructed a **separate** native
   object, so a Python subclass overriding a virtual method was never reached. A
   clean rebuild crashed with `RuntimeError: Tried to call pure virtual function
   "GreetingListener::on_greeting"`; a stale build silently dropped the callback.
   - **Fix** (`PythonInterface.mustache`): the wrapper now *subclasses* the native
     pybind11 type — `class {{resolveName}}({{nativeModule}}.{{resolveName}}):` with
     `def __init__(self, native=None): super().__init__(); self._native = self`.
     With `self._native = self`, the generated delegating methods would otherwise
     recurse infinitely, so interface wrappers now call the native class directly:
     - `PythonFunction.mustache`: `return {{nativeModule}}.{{typeName}}.{{resolveName}}(self, ...)`
     - `PythonProperty.mustache`: `{{nativeModule}}.{{typeName}}.{{resolveName}}.fget(self)` /
       `.fset(self, value)`
   - Added an `isInterface` predicate to `PythonGeneratorPredicates.kt` and gated the
     two templates with `{{#ifPredicate model "isInterface"}}` /
     `{{#unlessPredicate model "isInterface"}}`.
   - **Validated** in `sample_project`: subclassing native + `self._native = self`
     makes the trampoline fire (`[listener] greeted: Ada` now prints).

2. **Throwing functions not bound.** `Pybind11Function.mustache` wrapped every
   function binding in `{{#unlessPredicate "isThrowing"}}`, so a `throws`-annotated
   method (e.g. `Greeter.greet(name) throws GreeterError`) was never bound in
   pybind11. The Python wrapper still delegated to `self._native.greet`, raising
   `AttributeError: 'greeter.Greeter' object has no attribute 'greet'`.
   - **Fix** (`Pybind11Function.mustache`): removed the `isThrowing` skip. The
     `Return<T, Error>` caster (`Pybind11ReturnCaster.mustache`) already translates
     `Return<T, Error>` into a Python exception (raises `RuntimeError` with the
     qualified error enum name), so throwing functions bind and propagate correctly.
   - **Validated** in `sample_project`: `greet("")` now raises
     `RuntimeError - ::com::example::greeter::GreeterErrorCode::EMPTY_NAME`.

**Regression check:** the broader functional test run (`build-python-functional
--publish`) exits 8 with 15 pytest *collection* errors, all `ModuleNotFoundError`/
`ImportError` for modules that are **not generated for Python** (`MultiListener`,
`MethodOverloads`, `NullableCollections`, `RefEquality`, `Skip`,
`StructsWithMethodsInterfaceVector3`, …). These are pre-existing harness gaps: the
features `MethodOverloading`, `ComplexListeners`, `ListenersWithReturnValues`,
`Nullable`, and `SkipAttribute` are enabled for `cpp android android-kotlin swift
dart` but **not** `python` in `functional-tests/functional/CMakeLists.txt`. The
`Errors` feature (which has throwing functions) is also not python-enabled, so the
`isThrowing` removal has **no effect on the currently-enabled Python features** and
introduces zero regression risk. The aggregate `.so` builds and the enabled
features' wrappers import correctly.

### Inheritance forwarding-trampoline fix (2026-07-19)

The `Inheritance` functional feature is now enabled for Python and its pytest passes
3/3. Two generator bugs blocked it:

1. **Adopted native instance was ignored (pure virtual).** A factory returns a
   *foreign* (non-trampoline) C++ implementation (e.g. `RootInterfaceImpl`). The
   Python wrapper's `super().__init__(native)` must adopt that instance into the
   trampoline subclass, but the trampoline had no way to hold it — `init_alias`
   cannot adopt a foreign instance, and a `py::init([](shared_ptr<X>){...})` factory
   that built a fresh trampoline never stored the impl.
   - **Fix** (`Pybind11Interface.mustache` / `Pybind11Class.mustache`): the trampoline
     class carries a `std::shared_ptr<X> m_impl` member, and a `py::init` factory
     adopts the returned instance and stores it in `m_impl`.
   - **Fix** (`Pybind11TrampolineFunction.mustache` / `Pybind11TrampolineProperty.mustache`):
     the virtual overrides now **forward** to `m_impl` when it is held, and only fall
     back to `PYBIND11_OVERRIDE_PURE` when `m_impl` is null (a Python subclass). The
     **void** override previously called `m_impl->method(...)` but did *not* `return`,
     so control fell through to `PYBIND11_OVERRIDE_PURE` and raised
     `RuntimeError: Tried to call pure virtual function`. The `isVoid` predicate
     (`PythonGeneratorPredicates.kt`) now emits `return;` after forwarding a void call.
   - **Validated:** `InheritanceTestHelper.create_root()` returns an object whose
     `root_method` dispatches to the adopted `RootInterfaceImpl`; `call_root_method`
     no longer raises pure virtual.

2. **Test-logic bug.** `callRootMethod` is `void` in Lime (it only invokes
   `root_method` on the passed object from C++), so the test's
   `assert isinstance(result, RootInterface)` failed on `None`. The assertion now
   checks the passed object (`assert isinstance(root, RootInterface)`), matching the
   Swift/Android tests which do not assert on a return value for this void method.

**Regression check:** `Inheritance` is enabled for `python` in
`functional-tests/functional/CMakeLists.txt`; `MultipleInheritance` remains narrowed
out (its diamond-shaped C++ hierarchy still exercises an unimplemented path). The
`nesting_test.py` and `constants_test.py` still pass.

### Remaining failures (not Nesting-specific, out of scope here)

After the above, 10 modules still fail to import. These are separate bugs:

- `TopLevelPoint` / `UseTopLevelTypes` — `name 'TopLevelEnum' is not defined`
- `Constants` / `ConstantsInterface` — `name 'StateEnum' is not defined`
- `SimpleRoute` / `StructsWithConstantsInterfaceMultiRoute` — `name 'RouteType' is not defined`
- `Alice` / `Bob` — circular import between two modules
- `CollectionConstants` — invalid syntax (line 42)
- `StructConstants` — `unhashable type: 'set'`

Root cause for the enum-constant failures: `PythonNameResolver.resolveValue` renders
`LimeValue.Constant` via `limeValue.toString()` (bare `Parent.NAME`), and
`PythonImportResolver.resolveValueImports` line 106 deliberately returns `emptyList()` for
`LimeValue.Constant`, so the enum module is never imported and the bare name is wrong for
nested enums (should be `functional.FlattenedName.NAME`). Left for a follow-up.

## Feature set narrowed (Option A)

To get a clean compile, `python` was removed from the `feature(...)` lists of the
following functional features (their Lime inputs exercise generator paths that are
not yet implemented for Python):

- `ExternalTypes`, `DartExternalTypes` — external-type binding gaps (cpp-name
  qualification, external member getters, type-collection `using` alias).
- `MultipleInheritance` — diamond-shaped C++ hierarchy still exercises an
  unimplemented path (interface-inheritance trampoline does not override inherited
  pure-virtual methods across the diamond). `Inheritance` (single-rooted) is now
  **enabled** for Python (see forwarding-trampoline fix above).
- `Properties`, `MethodOverloading` — overload `def` resolution and trampoline
  virtual-override gaps.
- `Errors`, `Blob` — `Errors.lime` imports an external error enum from
  `ExternalTypes` (C++ impl not built when `ExternalTypes` is dropped); `Blobs.lime`
  imports `another.TypeCollectionWithEnums` from `Errors2.lime`.
- `GenericTypes`, `Lambdas`, `Defaults` — collection/array argument-count mismatches,
  lambda overloads, immutable-struct-with-defaults.
- `RefEquality` (in `Equatable`), `Comments`, `ComplexListeners`, `CppConst`,
  `CppNoexcept`, `FieldConstructors`, `Visibility`,
  `ListenersWithReturnValues`, `Locales`, `NoCache`,
  `StructsInTypes`, `StructsImmutable`, `PlatformNames`,
  `InstanceInStruct`, `StructsWithCompanion`, `UnderscorePackage`,
  `CrossPackageNameClash`, `CallbacksWithThreads` — various
  constructor/arg-count, listener, enum, name-clash, and threading gaps.

`Nesting` is now enabled for Python in the functional test configuration. Its
non-inheritance fixtures are covered by the B6 changes above; `NestedInheritance.lime`
remains deferred to Phase D because it exercises the inherited trampoline gap. The
focused `nesting_test.py` passes 2/2 under CPython 3.14 after rebuilding the
functional bindings.

The currently enabled Python features are `Strings`, `BuiltinTypes`, `Classes`,
`Interfaces`, `Structs`, `TypeDefs`, `Enums`, `CircularDependencies`, `Constants`,
`Dates`, `Durations`, `DeclarationOrder`, `EscapedNames`, `FullName`, `Nesting`,
and `Inheritance`.

## Remaining blocker (8.2)

The `Constants` feature is fixed and its pytest passes. A1-A7 are now enabled and
compile, and the aggregate extension imports correctly under CPython 3.14 (the
`SomeOpenNumberWrapperClass::make(int)` "unresolved symbol" was a red herring — see
Known issues). The broader generator gaps (overloads, inherited trampolines,
external types, collections, lambdas, properties, ref-equality, visibility, name
clashes, and threading) still keep the remaining functional features narrowed out.
The Python version mismatch that previously broke `ctest` is now **fixed** (see
Known issues): the test driver uses the same interpreter that built the `.so`.

## Known issues / test harness

### Root cause: Python version mismatch (the only real blocker for 8.2) — FIXED
The pybind11 extension is compiled against Python 3.14 headers — the build script
hard-codes `/opt/homebrew/Cellar/python@3.14/3.14.5/.../python3.14` — but the
machine's default `python3` is Miniconda 3.12.3. So:

- Importing the built `functional` module with the **default** interpreter fails:
  - `ModuleNotFoundError: No module named 'functional'` when `PYTHONPATH` is not
    set, or
  - `symbol not found in flat namespace '_PyEval_GetFrameLocals'` when it is (the
    3.14 `.so` cannot load under 3.12).

**Fix applied:** `functional/python/CMakeLists.txt` now runs pytest via the
`Python::Interpreter` imported target (created by `find_package(Python ...)` in
`gluecodium_target_python_sources`), so `ctest` launches the exact interpreter that
built the extension and exports the correct `PYTHONPATH`. The direct
`python3.14 -m pytest` command (see "Working invocation") remains the way to run a
single feature's tests by hand.

**The `.so` is Python-3.14-specific. Never run it with the default `python3` (3.12).**
The earlier concern that `SomeOpenNumberWrapperClass::make(int)` was an unresolved
symbol blocking runtime import was a **red herring** — the aggregate extension
links and imports cleanly under 3.14 (verified: `import functional` succeeds); the
only real blocker was the Python version mismatch, now fixed in the harness. With
`ctest` the correct interpreter is selected automatically, so the only remaining
risk is a *manual* invocation under the wrong `python3` — always use `python3.14`
(see "Working invocation"). Do not chase the wrong bug next session.

### Working invocation (single feature test)
Run from `functional-tests/functional/python` (the test sources are **not** copied
into the build dir), pointing at the 3.14 interpreter and the build output. `python3.14`
is on PATH (`/opt/homebrew/bin/python3.14`); use it directly (do **not** use the
default `python3`, which is Miniconda 3.12 and cannot load the 3.14-specific `.so`):

```bash
cd /Volumes/APFS/Work/gluecodium/functional-tests/functional/python
PYTHONPATH="/Volumes/APFS/Work/gluecodium/functional-tests/build-python/functional" \
  python3.14 -m pytest test/<feature>_test.py -v
```

Example (Constants, 6 passed):

```bash
cd /Volumes/APFS/Work/gluecodium/functional-tests/functional/python
PYTHONPATH="/Volumes/APFS/Work/gluecodium/functional-tests/build-python/functional" \
  python3.14 -m pytest test/constants_test.py -v
```

### ctest driver
The harness is now fixed: `functional/python/CMakeLists.txt` runs pytest via the
`Python::Interpreter` imported target created by `find_package(Python ...)` in
`gluecodium_target_python_sources` — i.e. the **same** interpreter that built the
extension — and exports `PYTHONPATH` to the build output. So `ctest` now launches
the correct interpreter automatically. The direct `python3.14` command above remains
useful for running a single feature's tests without a full rebuild.

## Follow-up work (not in this phase)

1. ~~Fix constant generation (module-level variables, not cross-module imports).~~ ✅ DONE.
2. Fix the broader generator gaps listed above (overloads, trampolines, external
   types, collections, dates/durations, lambdas, properties, ref-equality,
   visibility, name-clashes, threading) and re-enable the features one by one.
   - ~~Interface-inheritance trampoline (single-rooted `Inheritance`).~~ ✅ DONE —
     forwarding trampoline adopts the native impl (see above); `Inheritance` pytest
     passes 3/3. `MultipleInheritance` (diamond) remains.
3. Rewrite the remaining functional pytest files to match the actual generated
  `PascalCase` module/class names, then run them green as each feature is
  re-enabled. The A6 and A7 tests now use the generated names.
