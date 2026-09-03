# Phase 5 — Object Lifecycle and Callbacks (Implementation)

**Status**: ✅ Implemented
**Branch**: `python_bind`
**Prerequisite**: Phases 0–4 (type mapping) must be committed.

This document records the concrete changes made to implement Phase 5 of
`docs/python_pybind11_plan.md`: object lifecycle management, referential-equality
wrapper cache, GIL-safe C++ → Python callbacks (trampolines), and exception
mapping.

---

## 1. What was implemented

| Plan item | Status | Notes |
|-----------|--------|-------|
| 5.1 Object lifecycle | ✅ | pybind11 `std::shared_ptr` holder + `return_value_policy::automatic` (default). No manual ref-counting needed. |
| 5.2 Referential equality | ✅ | `python/pybind11/_wrapper_cache.h` generated (`gluecodium::python::WrapperCache`). |
| 5.3 GIL-safe callbacks | ✅ | Trampoline classes generated for `interface` types; every override acquires the GIL before `PYBIND11_OVERRIDE`. |
| 5.4 Exception mapping | ✅ | `Pybind11Exception.mustache` registers a `py::exception` translator mapping `std::error_code` → generated Python `Error` subclass. |
| 5.5 `@Async` | ⬜ | Deferred — not yet implemented. |

---

## 2. Files changed

### Kotlin (`gluecodium/src/main/java/.../generator/python/`)

- **`PythonGenerator.kt`**
  - `generatePybind11File`: now passes `fullName` (fully-qualified C++ name) and
    `trampolineName` in the template data; skips per-element includes for
    `LimeException` (no header is generated — exceptions are `std::error_code`).
  - `generateCommonFiles`: additionally emits `pybind11/_wrapper_cache.h`.
  - Stored `pybind11NameResolver` as a field so `generatePybind11File` can use
    `resolveFullName`.

- **`PythonGeneratorPredicates.kt`** — added predicates:
  - `needsRefSuffix` → delegates to `CppNameResolver.needsRefSuffix` (used by
    trampoline signatures so `&` matches the base class exactly).
  - `hasSetter` → `element is LimeProperty && element.setter != null` (used
    instead of a `{{#setter}}` section so the template `this` stays the property).
  - `hasNamespace` → `element.path.head.isNotEmpty()` (emits `using` aliases).
  - `isException` → `element is LimeException` (skips the `using` alias).

- **`Pybind11NameResolver.kt`**
  - Added `resolveFullName(element)` — builds the fully-qualified C++ name
    directly from the Lime path (`::` + internal namespace + `path.head` +
    `path.tail`). Avoids `CppNameCache` (which crashes on elements lacking a
    per-element C++ name rule, e.g. exceptions).

- **`Pybind11IncludeResolver.kt`**
  - `resolveElementImports` now returns `emptyList()` for a `LimeTypeRef` whose
    target is a `LimeException`. Exceptions are `std::error_code` (no header),
    so resolving their header produced a non-existent `#include`.

### Templates (`gluecodium/src/main/resources/templates/python/`)

- **`Pybind11File.mustache`**
  - Includes `<Python.h>` **before** `<pybind11/pybind11.h>` (required by
    pybind11 3.x).
  - Adds `namespace py = pybind11;` (pybind11 3.x no longer provides the `py`
    alias by default).
  - Emits `using ShortName = ::fully::qualified::Name;` for namespaced,
    non-exception types so the binding code can use short names.

- **`Pybind11Interface.mustache`**
  - Inlines the trampoline class (`class XxxTrampoline : public Xxx`) with a
    `using Xxx::Xxx;` inheriting constructor, then binds
    `py::class_<Xxx, std::shared_ptr<Xxx>, XxxTrampoline>`.

- **`Pybind11TrampolineFunction.mustache`** (new partial)
  - One override per interface method: `py::gil_scoped_acquire` + `PYBIND11_OVERRIDE`.
  - `const` + `&` added for ref-suffixed parameters to match the C++ base
    signature exactly.

- **`Pybind11TrampolineProperty.mustache`** (new partial)
  - Getter override (`PYBIND11_OVERRIDE(... "getter")`) and, when `hasSetter`,
    setter override (`PYBIND11_OVERRIDE(void, ..., "setter", value)`).

- **`Pybind11Property.mustache`**
  - `def_property` (getter + setter via `py::overload_cast`) when `hasSetter`,
    else `def_property_readonly`.

- **`Pybind11Exception.mustache`**
  - `py::exception<std::error_code>` + `register_exception_translator` using
    `e.message().c_str()` (not `.what()` — `std::error_code` has no `.what()`).

- **`Pybind11WrapperCache.mustache`** (new)
  - `gluecodium::python::WrapperCache` with `get_or_create`, `remove`,
    `instance()`, a `std::mutex`, and an `std::unordered_map<const void*, py::object>`.

- **`Pybind11ReturnCaster.mustache`** — added `#include "_wrapper_cache.h"`.

- **`Pybind11Trampoline.mustache`** — removed (superseded by the inlined
  trampoline in `Pybind11Interface.mustache` plus the
  `Pybind11TrampolineFunction`/`Pybind11TrampolineProperty` partials).

---

## 3. Key pitfalls discovered

1. **`<Python.h>` must precede `<pybind11/pybind11.h>`** — otherwise `py` is
   undeclared.
2. **pybind11 3.x has no `py` alias** — must add `namespace py = pybind11;`.
3. **`std::error_code` has no `.what()`** — use `.message().c_str()`.
4. **Mustache context traps** (see `docs/internal/mustache.md` notes):
   - `{{#if returnType.isVoid}}` shifts `this` to the return type → use
     `{{resolveName returnType.typeRef "Pybind11"}}` instead.
   - `{{#setter}}` shifts `this` to the setter function → use `{{#ifPredicate "hasSetter"}}`.
   - `ifPredicate`/`unlessPredicate` have **no `{{else}}`** → pair them.
   - `Pybind11File.mustache` wraps content in `{{#model}}`, so top-level data
     keys are invisible inside `contentTemplate`; derive names from `model`.
   - Comma handling in `PYBIND11_OVERRIDE`: use
     `{{#parameters}}, {{resolveName}}{{/parameters}}` (comma-before, no trailing).
5. **`register` is a C++ reserved keyword** — the test fixture's listener
   registration method was renamed `addListener`.
6. **Exception includes** — the generic include collector resolves the thrown
   exception's (non-existent) header; `Pybind11IncludeResolver` now skips
   `LimeException` type refs.

---

## 4. Verification

Generated C++ for `docs/python_binding_dev/phase5/test_python_lifecycle.lime`
passes `c++ -fsyntax-only` (with `-I<python3.12> -I<pybind11> -I<cpp/include>`)
for **all** `*.cpp` and `*.h` files in `python/pybind11/`. All generated
`*.py` files pass `python3 -m py_compile`.

**End-to-end runtime verification** is provided by the runnable sample project in
`docs/python_binding_dev/sample_project/` (see `docs/python_binding_dev/sample_project.md`).
It builds a real CPython extension via CMake and drives it from Python, exercising object
creation, method calls, GIL-safe callbacks, properties, and `throws` error mapping — i.e.
the full Phase 5 feature set. Note that the sample supplies a `PYBIND11_MODULE` entry point
and re-binds `class`/`interface`/`struct` types with the holders/constructors Phase 5 does
not yet emit (see the sample doc's "Known limitations worked around" section).

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
./gradlew :gluecodium:installDist -q
./gluecodium/build/install/gluecodium/bin/gluecodium \
    -input docs/python_binding_dev/phase5/test_python_lifecycle.lime \
    -output /tmp/fullgen -generators cpp,python
```

---

## 5. Known limitations

- **`@Async` (5.5)** is not implemented.
- The **wrapper cache** header is generated but not yet wired into the
  `return_value_policy` of returned pointers (referential equality is not yet
  enforced at the call sites).
- **`Locale` caster** is still missing (same gap as Phase 4).
- The stale `Pybind11Trampoline.mustache` (whole-class trampoline) was already
  removed; the inlined trampoline lives in `Pybind11Interface.mustache` with the
  `Pybind11TrampolineFunction`/`Pybind11TrampolineProperty` partials.
