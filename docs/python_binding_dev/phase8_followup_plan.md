# Phase 8 Follow-up: Re-enabling Narrowed Functional Features for Python

> **Date**: 2026-07-13
> **Branch**: `python_bind`
> **Status**: Planning
> **Related**: [phase8_status.md](./phase8_status.md), [python_pybind11_plan.md](../python_pybind11_plan.md)
> **Scope**: All narrowed features **except** `Dates` and `Durations` (those are being fixed in a separate ongoing session)

---

## 1. Overview

Phase 8 narrowed ~40 functional features out of the `python` generator list to achieve a clean compile. The first follow-up work has re-enabled `BuiltinTypes`, `Strings`, and `Enums`; `Dates` and `Durations` are tracked separately. This document describes a phased plan to re-enable the remaining features, ordered by their inter-feature and generator-capability dependencies.

### 1.1 Root-Cause Categories

All narrowed features fall into one or more of these generator-gap categories:

| Gap ID | Description | Affected Features |
|--------|-------------|-------------------|
| **G1** | Constructor/argument-count template bugs — pybind11 `def()` / `init()` calls with wrong arg count or missing overload resolution | BuiltinTypes, Strings, Enums, Structs, Classes, Interfaces, TypeDefs, InstanceInStruct, StructsInTypes, StructsImmutable, StructsWithCompanion, FieldConstructors, Nesting |
| **G2** | Property binding — `def_property()` / `def_property_static()` not emitted or wrong accessor names | Properties, NoCache, CppConst, CppNoexcept |
| **G3** | Inheritance trampoline — inherited pure-virtual methods not overridden in `Trampoline` class, causing abstract-class instantiation failure | Inheritance, MultipleInheritance, MethodOverloading, RefEquality, Visibility |
| **G4** | Method overloading — Python does not support overloaded method names; `pybind11::overload_cast` or renamed overloads not implemented | MethodOverloading, Properties, Defaults |
| **G5** | Generic/collection type binding — `List<T>`, `Map<K,V>`, `Set<T>` with user-defined `T` not correctly converted via pybind11 type casters | GenericTypes, Lambdas, Defaults, Locales, RefEquality |
| **G6** | External type binding — `external { cpp include ...; cpp name ... }` not resolved in pybind11 includes/qualified names | ExternalTypes, DartExternalTypes, Defaults, Errors |
| **G7** | Error/exception handling — `Return<T, Error>` → Python exception translation not fully wired for all error enum patterns | Errors, Blob |
| **G8** | Lambda/callback binding — `lambda` types not wrapped as `py::cpp_function` / `std::function` | Lambdas, ComplexListeners, ListenersWithReturnValues, CallbacksWithThreads |
| **G9** | Visibility/internal filtering — `@Internal` elements not correctly skipped/retained in Python output | Visibility, Comments |
| **G10** | Naming/package resolution — underscore packages, cross-package name clashes, platform names | UnderscorePackage, CrossPackageNameClash, PlatformNames |
| **G11** | Doc comment preservation — `//` comments not propagated to Python docstrings | Comments |
| **G12** | Threading/GIL — callbacks from non-Python threads need `py::gil_scoped_acquire` | CallbacksWithThreads |
| **G13** | Referential equality — wrapper cache not used for `@Equatable` / `RefEquality` | RefEquality, Equatable |
| **G14** | Locale type — `Locale` basic type not bound (currently mapped to `str` placeholder) | Locales |

### 1.2 Inter-Feature Dependency Graph

```
ExternalTypes (G6) ─────────────────────────┐
  ├── Errors (G6, G7)                       │
  │    ├── Blob (G7)                        │
  │    └── Inheritance/ConstructorOverride  │
  │         (G3, G4)                        │
  └── Defaults (G5, G6)                     │
                                            │
GenericTypes (G5) ──────────────────────────┤
  ├── Lambdas (G5, G8)                      │
  ├── Locales (G5, G14)                     │
  ├── Defaults (G5, G6)                     │
  ├── RefEquality (G5, G13)                 │
  └── Inheritance (G5, G3)                  │
                                            │
Inheritance (G3) ───────────────────────────┤
  ├── MultipleInheritance (G3)              │
  ├── MethodOverloading (G3, G4)            │
  ├── Properties (G2, G3, G4)               │
  ├── RefEquality (G3, G13)                 ├──► Phase 6: Listeners & Threading
  ├── ComplexListeners (G3, G8)             │    ComplexListeners, ListenersWithReturnValues,
  ├── ListenersWithReturnValues (G3, G8)    │    CallbacksWithThreads
  ├── Visibility (G3, G9)                   │
  └── Nesting/NestedInheritance (G3)        │
                                            │
Properties (G2) ────────────────────────────┤
  ├── MethodOverloading (G2, G4)            │
  ├── CppConst (G2)                         │
  ├── CppNoexcept (G2)                      │
  └── NoCache (G2)                          │
                                            │
G1 (constructor/arg-count) is foundational ─┘
and unblocks: BuiltinTypes, Strings, Enums,
Structs, Classes, Interfaces, TypeDefs, etc.
```

---

## 2. Implementation Phases

### Phase A — Basic Type System (G1) [No dependencies]

**Goal**: Fix constructor/argument-count template bugs so that simple classes, structs, enums, and typedefs compile and bind correctly.

These features have no cross-feature Lime imports and exercise only the most basic pybind11 binding paths (static functions, instance methods, constructors, struct fields). The root cause is likely in `Pybind11Function.mustache`, `Pybind11Struct.mustache`, and `Pybind11Class.mustache` templates emitting wrong argument lists.

| Order | Feature | Lime Files | Key Gap | Estimated Effort |
|-------|---------|------------|---------|-----------------|
| A1 | `BuiltinTypes` | `StaticBooleanMethods.lime`, `StaticFloatDoubleMethods.lime`, `StaticIntMethods.lime` | G1: static function arg count | Small |
| A2 | `Strings` | `StaticStringMethods.lime`, `StringsWithCstring.lime`, `CppRefReturnType.lime` | G1: static function arg count + C++ ref return type | Small |
| A3 | `Enums` | `Enums.lime`, `EnumeratorAlias.lime`, `EnumOptionSet.lime`, `EnumsTypeCollection.lime` | G1: native enum bridge, nested/type-collection enum registration, and enum-valued struct conversion | Small |
| A4 | `TypeDefs` | `StaticTypedef.lime` | G1: typealias binding | Small |
| A5 | `Structs` | `Structs.lime`, `Accessors.lime` | G1: struct field binding + accessors | Small |
| A6 | `Classes` | `Instances.lime` | G1: class constructor + instance methods | Small |
| A7 | `Interfaces` | `Interfaces.lime` | G1: interface trampoline + factory functions | Medium |

**Verification**: For each feature, re-enable `python` in the `feature(...)` call in `functional/CMakeLists.txt`, rebuild, and run the corresponding pytest file.

**A3 implementation status (2026-07-14):** ✅ Generator support is implemented. Nested enum LIME types are flattened into per-type Python and pybind11 files, all nested enum registrations are added to the module initializer, and Python enum members retain their native pybind11 values through `_native`. Enum-valued struct constructors and fields unwrap and wrap those native values correctly. The generated A3 Python wrappers pass `py_compile`, and the separate unresolved `DurationInterface::duration_function` symbol is fixed by the Python interface binding. The full functional pytest remains blocked by the existing generated-module import mismatch (`test.durations` versus PascalCase modules) and missing nested `DurationStruct` wrapper.

**Exit criteria**: All 7 features compile, link, and their pytest files pass (after rewriting test imports to match generated PascalCase module names).

---

### Phase B — Structs & Nesting (G1) [Depends on Phase A]

**Goal**: Extend struct binding to cover immutable structs, structs in type collections, structs with companion methods/constants, field constructors, and nested types.

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| B1 | `StructsImmutable` | `PlainDataStructuresImmutable.lime` | G1: `@Immutable` struct constructor (all-fields init) | A5 | Small |
| B2 | `StructsInTypes` | `StructsFromTypeCollection.lime`, `TypeCollection.lime` | G1: type-collection struct binding | A5 | Small |
| B3 | `StructsWithCompanion` | `StructsWithMethods.lime`, `StructsWithConstants.lime` | G1: struct with methods + constants | A5, Constants(✅) | Small |
| B4 | `FieldConstructors` | `FieldConstructors.lime`, `FieldConstructorsInit.lime`, `FieldConstructorsNesting.lime` | G1: field constructor binding | A5 | Medium |
| B5 | `InstanceInStruct` | `StructWithInstance.lime` | G1: struct containing class instance pointers | A5, A6 | Small |
| B6 | `Nesting` | `TopLevelTypes.lime`, `NestedContainers.lime`, `NestedClassWithProperty.lime`, `NestingInStruct.lime`, `NestedInheritance.lime` | G1+G3: nested types (skip `NestedInheritance.lime` for now, handle in Phase D) | A5, A6, A7 | Medium |

**Note**: `Nesting` includes `NestedInheritance.lime` which exercises inheritance (G3). If G3 is not yet fixed, temporarily `@Skip(Python)` that specific Lime file and re-enable it in Phase D.

**Exit criteria**: All 6 features compile and pass pytest.

---

### Phase C — Properties & Const/Noexcept (G2) [Depends on Phase A]

**Goal**: Implement property binding (`def_property` / `def_property_static` / `def_readwrite`) and handle `@Cpp(Const)` / `@Cpp(Noexcept)` method attributes.

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| C1 | `Properties` | `Attributes.lime`, `AttributesInterface.lime`, `AttributesInterfaceFactory.lime` | G2: `def_property` for get/set, static properties, interface property trampoline | A6, A7 | Medium |
| C2 | `CppConst` | `CppConstMethods.lime` | G2: const method binding (no special pybind11 action needed, but template must not emit non-const override) | A6 | Small |
| C3 | `CppNoexcept` | `CppNoexceptMethods.lime` | G2: noexcept method binding | A6 | Small |
| C4 | `NoCache` | `NoCache.lime` | G2: `@Cached` property handling (may need no-op for Python or use `def_property_cached`) | C1 | Small |

**Verification**: Re-enable each feature, rebuild, run pytest.

**Exit criteria**: All 4 features compile and pass pytest.

---

### Phase D — Inheritance & Overloading (G3, G4) [Depends on Phase A, C]

**Goal**: Fix the trampoline class to override all inherited pure-virtual methods, and implement overload resolution for Python (since Python does not support method overloading natively).

#### D1: Inheritance Trampoline Fix (G3)

**Problem**: The `Pybind11TrampolineFunction.mustache` template only overrides methods directly declared on the current container, not methods inherited from parent interfaces/classes. This makes the trampoline class abstract, preventing pybind11 from instantiating it.

**Fix**: In `Pybind11Interface.mustache` and `Pybind11Class.mustache`, iterate over `inheritedFunctions` (already available via `LimeContainerWithInheritance.inheritedFunctions`) in addition to `functions` when emitting trampoline overrides.

**Affected templates**:
- `Pybind11Interface.mustache` — add `{{#inheritedFunctions}}` trampoline section
- `Pybind11Class.mustache` — add `{{#inheritedFunctions}}` trampoline section
- `Pybind11TrampolineFunction.mustache` — ensure it handles inherited functions correctly

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| D1 | `Inheritance` | `Inheritance.lime`, `InheritanceNameClash.lime`, `ListenerInheritance.lime`, `ListenerInheritanceArrays.lime`, `CrossPackageInheritance.lime`, `InterfaceWithLambda.lime`, `ConstructorOverride.lime` | G3: trampoline override for inherited pure-virtual methods. **Note**: `ConstructorOverride.lime` imports `ThrowingConstructor.Some` from `Errors.lime` — needs `@Skip(Python)` on that sub-file or Phase E first. `ListenerInheritanceArrays.lime` needs GenericTypes (G5). `InterfaceWithLambda.lime` needs Lambdas (G8). | A6, A7, C1 | Large |
| D2 | `MultipleInheritance` | `MultipleInheritance.lime` | G3: narrow interface + multiple parent trampolines | D1 | Medium |
| D3 | `MethodOverloading` | `MethodOverloads.lime`, `InheritanceOverloads.lime` | G4: overload resolution — Python does not support overloaded names. Use `pybind11::overload_cast<...>()` or `@Python(Name=...)` attribute to rename. Currently `PythonOverloadsValidator` only warns; needs actual rename or `py::overload_cast` in template. | D1, C1 | Large |

**Important dependency notes for `Inheritance`**:
- `ConstructorOverride.lime` references `ThrowingConstructor.Some` from `Errors.lime`. Options:
  1. Temporarily `@Skip(Python)` the `ChildConstructorOverloads` class and handle it after Phase E.
  2. Or do Phase E (Errors) before D1.
- `ListenerInheritanceArrays.lime` uses `List<ParentListener>` — needs G5 (GenericTypes). Can temporarily skip or do after Phase F.
- `InterfaceWithLambda.lime` uses a `lambda` type — needs G8 (Lambdas). Can temporarily skip or do after Phase G.
- **Recommendation**: Do D1 with temporary `@Skip(Python)` on the 3 problematic sub-files, then revisit after Phases E, F, G.

**Exit criteria**: `Inheritance` (minus 3 skipped sub-files), `MultipleInheritance`, `MethodOverloading` compile and pass pytest.

---

### Phase E — External Types & Error Handling (G6, G7) [Depends on Phase D]

**Goal**: Support `external { cpp include ...; cpp name ... }` descriptors in pybind11 binding generation, and wire up `Return<T, Error>` → Python exception translation for all error patterns.

#### E1: External Type Binding (G6)

**Problem**: The pybind11 binding generator does not resolve `external` descriptors. When a LIME type has `external { cpp include "include/ExternalTypes.h" }`, the pybind11 binding file needs to:
1. `#include` the external header (not the generated C++ header)
2. Use the external C++ name (e.g. `::external::even_more_external::AlienStruct`) instead of the generated name
3. Skip generating a Python wrapper for the external type (it is opaque or pre-existing)

**Affected files**:
- `Pybind11IncludeResolver.kt` — resolve includes for external types
- `Pybind11NameResolver.kt` — resolve C++ names for external types
- `PythonImportResolver.kt` — resolve Python imports for external types (use `external.python.importPath` descriptor)
- `Pybind11Class.mustache` / `Pybind11Struct.mustache` / `Pybind11Enum.mustache` — skip binding generation for external types or emit opaque type caster

#### E2: Error/Exception Handling (G7)

**Problem**: `Return<T, Error>` → Python exception translation is partially implemented (the `Pybind11ReturnCaster.mustache` was fixed in Phase 8), but error enum patterns (internal, external, cross-package) are not fully tested.

**Affected files**:
- `Pybind11Exception.mustache` — exception binding (translate `std::error_code` → Python exception)
- `Pybind11Function.mustache` — unwrap `Return<T, Error>` and throw on error
- `Pybind11ReturnCaster.mustache` — type caster for `Return<T, Error>`

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| E1 | `ExternalTypes` | `ExternalTypes.lime`, `ExternalImmutable.lime`, `ExternalClassAsInterface.lime`, `UseExternalTypes.lime` | G6: external type C++ name/include resolution | D1 | Large |
| E2 | `DartExternalTypes` | `DartExternalTypes.lime` | G6: same as E1 but Dart-specific external types (should be covered by E1 fix) | E1 | Small |
| E3 | `Errors` | `Errors.lime`, `Errors2.lime`, `ErrorsInInterface.lime`, `ErrorsWithNonTrivialType.lime` | G7: `Return<T, Error>` exception translation for internal/external/cross-package error enums. **Depends on E1** because `Errors.lime` has `ExternalErrorCode` with `external { cpp include "include/ExternalTypes.h" }` | E1 | Large |
| E4 | `Blob` | `Blobs.lime`, `StaticByteArrayMethods.lime` | G7: `Blobs.lime` imports `another.TypeCollectionWithEnums.Explosive` from `Errors2.lime` — needs E3 first. Also `Blob` type = `List<UByte>` which needs G5. | E3, F1 | Medium |

**Exit criteria**: All 4 features compile and pass pytest.

---

### Phase F — Generic/Collection Types (G5) [Depends on Phase A]

**Goal**: Support `List<T>`, `Map<K,V>`, `Set<T>` with user-defined element types in pybind11 bindings.

**Problem**: pybind11 has built-in support for `std::vector<T>`, `std::map<K,V>`, `std::set<T>` via `<pybind11/stl.h>`. The gap is that user-defined types wrapped by Gluecodium are not directly compatible with pybind11's STL converters — the wrapper type needs to be unwrapped to its C++ representation.

**Fix**: Ensure that `Pybind11NameResolver` resolves generic type parameters to their C++ representation (e.g. `std::vector<::test::MyClass*>`), and that the pybind11 type caster for the wrapper class is registered before the STL container caster is used.

**Affected files**:
- `Pybind11NameResolver.kt` — resolve `LimeList` → `std::vector<...>`, `LimeMap` → `std::map<...>`, `LimeSet` → `std::set<...>`
- `Pybind11Function.mustache` — ensure argument types for collections use C++ STL types
- Ensure `#include <pybind11/stl.h>` is in the common header

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| F1 | `GenericTypes` | `Arrays.lime`, `SetType.lime`, `Maps.lime`, `NestedGenericTypes.lime`, `OptimizedList.lime` | G5: `List`/`Map`/`Set` with user-defined types + nested generics | A6, A7 | Large |
| F2 | `Defaults` | `Defaults.lime`, `DefaultsWithFcStruct.lime`, `PositionalDefaults.lime`, `PositionalEnumerators.lime`, `InternalEnumDefaults.lime`, `FireConstants.lime`, `ConstantDefaults.lime` | G5+G6: collection defaults + external enum defaults. **Depends on E1** for `ExternalEnum` with `external { cpp include "include/ExternalTypes.h" }` | E1, F1 | Large |

**Exit criteria**: Both features compile and pass pytest.

---

### Phase G — Lambdas/Callbacks (G8) [Depends on Phase D, F]

**Goal**: Bind LIME `lambda` types as Python callables (`py::cpp_function` / `std::function`).

**Problem**: LIME lambdas map to `std::function<Signature>` in C++. pybind11 supports converting Python callables to `std::function` automatically, but the generator needs to:
1. Generate a type alias/typedef for the `std::function` type
2. Register the lambda type so pybind11 can convert it
3. Handle nullable lambdas (`std::optional<std::function<...>>`)

**Affected files**:
- `Pybind11Lambda.mustache` — lambda type binding (register `std::function` type alias)
- `Pybind11Function.mustache` — function arguments of lambda type
- `PythonLambda.mustache` — Python-side lambda type alias (`Callable[...]`)
- `PythonNameResolver.kt` — resolve lambda types to `Callable[...]` in type stubs

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| G1 | `Lambdas` | `Lambdas.lime` | G8: lambda type binding, nullable lambdas, lambda in struct fields, overloaded lambdas (`@Overloaded`), lambda composition | D1, F1 | Large |

**Exit criteria**: `Lambdas` compiles and passes pytest.

---

### Phase H — Naming, Visibility & Docs (G9, G10, G11) [Depends on Phase D]

**Goal**: Handle `@Internal` visibility filtering, `@Python(Name=...)` platform names, underscore package names, cross-package name clashes, and doc comment preservation.

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| H1 | `PlatformNames` | `PlatformNames.lime` | G10: `@Python(Name=...)` attribute — ensure name resolver respects Python platform name | A6 | Small |
| H2 | `Visibility` | `VisibilityAttribute.lime`, `VisibilityInternal.lime`, `VisibilityPlatform.lime`, `VisibilityPlatformReverse.lime`, `InternalFields.lime` | G9: `@Internal` filtering — skip internal elements in Python output, handle internal fields in structs, internal constructors, internal inheritance. **Depends on D1** for `InternalAttributeClassInherits` | D1 | Medium |
| H3 | `UnderscorePackage` | `UnderscorePackage.lime`, `UseUnderscorePackage.lime` | G10: package name `test_off` → Python module path `test_off` (ensure no name mangling) | A6 | Small |
| H4 | `CrossPackageNameClash` | `CrossPackageNameClashA.lime`, `CrossPackageNameClashB.lime`, `CrossPackageNameClashC.lime` | G10: same type name in different packages (`test.Alphabet`, `test.foo.Alphabet`, `test.bar.Alphabet`) — ensure Python import paths don't collide | A6 | Small |
| H5 | `Comments` | `Comments.lime`, `CommentsInterface.lime` | G11: doc comment preservation — propagate `//` comments to Python docstrings via `PythonCommentsProcessor` | A6, A7 | Medium |

**Exit criteria**: All 5 features compile and pass pytest.

---

### Phase I — Equality & Locale (G13, G14) [Depends on Phase D, F]

**Goal**: Implement referential equality (wrapper cache) and locale type binding.

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| I1 | `Equatable` (including `RefEquality`) | `Equatable.lime`, `RefEquality.lime`, `SimpleEquality.lime` | G13: `@Equatable` struct equality + `RefEquality` wrapper cache for class instances. `RefEquality.lime` uses `DummyChildClass : DummyParentClass` (needs D1) and `List<DummyClass>` (needs F1) | D1, F1 | Medium |
| I2 | `Locales` | `Locales.lime`, `LocaleDefaults.lime` | G14: `Locale` basic type — currently mapped to `str` in `PythonNameResolver`. Need proper locale binding (likely `str` with BCP-47 tag, matching the Dart/Swift approach). Also uses `List<Locale>` (needs F1) | F1 | Medium |

**Exit criteria**: Both features compile and pass pytest.

---

### Phase J — Listeners & Threading (G8, G12) [Depends on Phase D, G]

**Goal**: Bind complex listener patterns, listeners with return values, and thread-safe callbacks.

| Order | Feature | Lime Files | Key Gap | Deps | Effort |
|-------|---------|------------|---------|------|--------|
| J1 | `ComplexListeners` | `ComplexListeners.lime` | G8: complex callback patterns (multi-method listeners, listener composition) | D1, G1 | Medium |
| J2 | `ListenersWithReturnValues` | `ListenersReturnValues.lime`, `ListenerWithAttributes.lime`, `ListenerInternal.lime` | G8: listeners that return values (trampoline must call back into Python and return the result) + listener with attributes (property on interface) | D1, G1, C1 | Medium |
| J3 | `CallbacksWithThreads` | `ListenersThreads.lime` | G12: callbacks from non-Python threads — need `py::gil_scoped_acquire` in trampoline methods. **This is the most complex feature** as it requires modifying the trampoline template to acquire the GIL before calling back into Python. | D1, G1 | Large |

**Exit criteria**: All 3 features compile and pass pytest.

---

### Phase K — Cleanup & Revisit Skipped Sub-files [Depends on all above]

**Goal**: Re-enable the temporarily skipped sub-files from Phase D and verify the full feature set.

| Order | Task | Description | Deps | Effort |
|-------|------|-------------|------|--------|
| K1 | Re-enable `ConstructorOverride.lime` | Part of `Inheritance` feature — references `ThrowingConstructor.Some` from `Errors.lime` | D1, E3 | Small |
| K2 | Re-enable `ListenerInheritanceArrays.lime` | Part of `Inheritance` feature — uses `List<ParentListener>` | D1, F1 | Small |
| K3 | Re-enable `InterfaceWithLambda.lime` | Part of `Inheritance` feature — uses `lambda` type | D1, G1 | Small |
| K4 | Re-enable `NestedInheritance.lime` | Part of `Nesting` feature — uses nested inheritance | D1, B6 | Small |
| K5 | Full regression | Run all ~40 functional pytest files and ensure they pass | All | Medium |

**Exit criteria**: All functional features are enabled for `python`, all pytest files pass.

---

## 3. Summary: Phase Dependency Diagram

```
Phase A (Basic Types) ──────┬──► Phase B (Structs & Nesting)
                             ├──► Phase C (Properties & Const)
                             ├──► Phase F (Generic Types)
                             │         │
Phase C (Properties) ────┐   │         ▼
                         ├───┼──► Phase D (Inheritance & Overloading)
Phase A ─────────────────┘   │         │
                             │    ┌────┼────┬────────┬────────┐
                             ▼    ▼    ▼    ▼        ▼        ▼
Phase D ──────────► Phase E (External)  Phase G   Phase H  Phase I
                         │              (Lambdas)  (Naming) (Eq/Locale)
                         ▼                │
                    Phase F (Defaults)    │
                                        ▼
                                  Phase J (Listeners & Threading)
                                        │
                                        ▼
                                  Phase K (Cleanup)
```

## 4. Effort Estimates

| Phase | Features | Estimated Effort | Key Risk |
|-------|----------|-----------------|----------|
| A | 7 | 3-4 days | Low — template arg-count fixes |
| B | 6 | 2-3 days | Low — struct variant binding |
| C | 4 | 2-3 days | Medium — property trampoline for interfaces |
| D | 3 | 5-7 days | **High** — trampoline rewrite + overload resolution |
| E | 4 | 4-5 days | **High** — external type system is complex |
| F | 2 | 3-4 days | Medium — STL container type caster interaction |
| G | 1 | 3-4 days | Medium — `std::function` conversion |
| H | 5 | 2-3 days | Low — naming/visibility filtering |
| I | 2 | 2-3 days | Medium — wrapper cache + locale |
| J | 3 | 4-5 days | **High** — GIL/threading |
| K | 5 tasks | 1-2 days | Low — cleanup |
| **Total** | **~40** | **~30-40 days** | |

## 5. Key Design Decisions to Make

### 5.1 Overload Resolution (G4)

Python does not support overloaded method names. Two options:

1. **`pybind11::overload_cast<Args...>()`** — pybind11's built-in overload resolution. Requires that the C++ methods are actually overloaded (which they are, since C++ supports overloading). This is the cleanest approach but requires the template to emit `py::overload_cast<arg_types>(&Class::method)` for each overload.

2. **`@Python(Name=...)` rename** — require users to annotate overloaded methods with distinct Python names. This is already supported by the `PythonOverloadsValidator` (which warns), but would require updating all functional test Lime files.

**Recommendation**: Use `py::overload_cast` (option 1) for automatic resolution, and fall back to `@Python(Name=...)` for ambiguous cases.

### 5.2 External Type Binding (G6)

External types have `external { cpp include "..."; cpp name "..." }` descriptors. Options:

1. **Opaque binding** — register the external type as an opaque Python type with a custom type caster that converts between the C++ type and a Python wrapper.
2. **Skip binding** — do not generate a Python wrapper for external types; only emit the C++ include and use the C++ type directly in function signatures.

**Recommendation**: Option 2 for now (skip binding, use C++ type directly). The external type is already defined in C++ and pybind11 will treat it as an opaque pointer type. Users can wrap it manually if needed.

### 5.3 Threading/GIL (G12)

For callbacks from non-Python threads, the trampoline must acquire the GIL before calling into Python. Options:

1. **Always acquire GIL** — wrap every trampoline method body with `py::gil_scoped_acquire`. Safe but has performance overhead.
2. **Conditional GIL** — only acquire for features marked with `@CallbacksWithThreads` or a similar attribute.

**Recommendation**: Option 1 (always acquire) for correctness. The performance overhead is negligible for the functional tests, and it is the safest default. Can be optimized later if needed.

### 5.4 Locale Type (G14)

The `Locale` basic type is currently mapped to `str` in `PythonNameResolver`. Options:

1. **String representation** — use `str` with BCP-47 language tag (e.g. `"en-US"`). This matches the Dart/Swift approach and is simple.
2. **`locale` module** — use Python's `locale` module. More native but less portable.

**Recommendation**: Option 1 (string with BCP-47 tag). This is the simplest and most portable approach, and matches what other generators do.

---

## 6. Testing Strategy

For each phase:

1. **Re-enable the feature** in `functional/CMakeLists.txt` by adding `python` to the `feature(...)` generator list.
2. **Rebuild** the extension module:
   ```bash
   cd functional-tests
   ./scripts/build-python-functional --publish
   ```
3. **Rewrite pytest files** to match the actual generated module/class names (PascalCase modules).
4. **Run pytest**:
   ```bash
   cd build-python/functional/python
   PYTHONPATH=".../build-python/functional" python3 -m pytest tests/<feature>_test.py -v
   ```
5. **Fix generator bugs** iteratively until the test passes.
6. **Run smoke tests** to ensure no regressions:
   ```bash
   ./gradlew test
   ```

---

## 7. Appendix: Feature-to-Gap Mapping

| Feature | Gaps | Phase | Notes |
|---------|------|-------|-------|
| BuiltinTypes | G1 | A | Static int/float/bool methods |
| Strings | G1 | A | Static string methods, C++ ref return |
| Enums | G1 | A | Enum + type collection enum |
| TypeDefs | G1 | A | Typealias binding |
| Structs | G1 | A | Basic struct + accessors |
| Classes | G1 | A | Class constructor + instance methods |
| Interfaces | G1 | A | Interface trampoline + factory |
| StructsImmutable | G1 | B | `@Immutable` struct |
| StructsInTypes | G1 | B | Type collection struct |
| StructsWithCompanion | G1 | B | Struct with methods/constants |
| FieldConstructors | G1 | B | Field constructor variants |
| InstanceInStruct | G1 | B | Struct with class instance field |
| Nesting | G1, G3 | B, K | Nested types (inheritance part in K) |
| Properties | G2, G3 | C | `def_property`, static, interface |
| CppConst | G2 | C | Const method binding |
| CppNoexcept | G2 | C | Noexcept method binding |
| NoCache | G2 | C | `@Cached` property |
| Inheritance | G3 | D, K | Trampoline override (3 sub-files in K) |
| MultipleInheritance | G3 | D | Narrow interface + multiple parents |
| MethodOverloading | G3, G4 | D | Overload resolution |
| ExternalTypes | G6 | E | External type binding |
| DartExternalTypes | G6 | E | Same as ExternalTypes |
| Errors | G6, G7 | E | `Return<T,Error>` exception translation |
| Blob | G7, G5 | E, F | Blob + Explosive exception from Errors2 |
| GenericTypes | G5 | F | List/Map/Set with user types |
| Defaults | G5, G6 | F | Collection defaults + external enum |
| Lambdas | G5, G8 | G | `std::function` binding |
| PlatformNames | G10 | H | `@Python(Name=...)` |
| Visibility | G3, G9 | H | `@Internal` filtering |
| UnderscorePackage | G10 | H | `test_off` package |
| CrossPackageNameClash | G10 | H | Same name in different packages |
| Comments | G11 | H | Doc comment → Python docstring |
| Equatable/RefEquality | G3, G5, G13 | I | Equality + wrapper cache |
| Locales | G5, G14 | I | Locale type binding |
| ComplexListeners | G3, G8 | J | Complex callback patterns |
| ListenersWithReturnValues | G3, G8 | J | Listeners with return values |
| CallbacksWithThreads | G8, G12 | J | GIL management |
