# Phase 4 — Type Mapping (Implementation)

> **Status**: ✅ Completed (not yet committed)
> **Date**: 2026-07-13
> **Source plan**: `docs/python_pybind11_plan.md` (Phase 4, lines 322–372)
> **Build**: `gluecodium` compiles; `-generators python` produces correct Python + pybind11 output
> for all basic, compound, and user-defined types.

## Goal

Complete the Python/pybind11 type mapping so that every LIME type (basic, compound, nullable,
user-defined, typealias, lambda) resolves to the correct Python annotation and the correct C++
type in the pybind11 binding code. Wire the proven `Return<T, Error>` caster (Phase 0 spike) as a
generated common header.

## Changes

### `PythonNameResolver.kt`
- **Basic types** (was a placeholder): `Date → datetime.datetime`, `Duration → datetime.timedelta`,
  `Locale → str`; the existing `Void/Bool/String/Blob/Float/Double/int` mappings retained.
- **Compound types**: `LimeList → list[E]`, `LimeSet → set[E]`, `LimeMap → dict[K, V]`
  (recursively resolving element types).
- **Type alias**: `LimeTypeAlias → resolveName(typeRef)` (maps to the underlying Python type).
- `LimeReturnType` still delegates to its `typeRef`.

### `PythonImportResolver.kt`
- `Date` / `Duration` now emit a `PythonImport("datetime")` (so `datetime.datetime` /
  `datetime.timedelta` annotations resolve).
- Generic (container) types are recognized as builtins and produce **no** import (previously they
  were mis-resolved as user-defined types, yielding bogus `from list[str] import list[str]` lines).

### `Pybind11File.mustache`
- Added `#include <pybind11/chrono.h>` alongside `<pybind11/stl.h>` so `Date`/`Duration` convert
  automatically (per the Phase 0 chrono spike).

### `PythonGenerator.kt`
- `generateCommonFiles()` now also emits `pybind11/_return_caster.h` — the custom
  `type_caster<::Return<Value, Error>>` (templated on the generated `Return.h` include path, which
  follows the C++ internal namespace, e.g. `lorem_ipsum/Return.h` or `Return.h` when no internal
  namespace is set).

### `Pybind11ReturnCaster.mustache` (new common file)
- The exact caster proven in `docs/python_binding_dev/spike_return_caster.md`, generalized to
  `::Return<Value, Error>` (the generated adapter lives in the global namespace inside
  `Return.h`). On success it delegates to pybind11's built-in value caster; on failure it raises
  `RuntimeError` carrying the error string (via `ReturnErrorToString` traits, specialized for
  `std::error_code`). `load()` returns `false` (output-only adapter).

### Templates fleshed out
- `PythonTypeAlias.mustache`: `Name = <underlying Python type>` (re-export).
- `PythonLambda.mustache`: `Name = Callable[[param_types...], return_type]` (uses `typing.Callable`).
- `Pybind11TypeAlias.mustache` / `Pybind11Lambda.mustache`: unchanged (no binding needed — typealias
  is transparent; lambda is a `std::function` handled inline where used).

## Verification

### Compile-time
- `./gradlew :gluecodium:compileKotlin` → success.
- `./gradlew :gluecodium:installDist` → success.

### Runtime (end-to-end)
Generated on `docs/python_binding_dev/phase4/test_python_types.lime` (struct, interface, class with
Date/Duration/Locale/List/Map/Set/nullable, typealias, lambda), `-generators python`:

- **All `.py` files pass `python3 -m py_compile`.**
- Sample `Calculator.py` type annotations (correct):
  ```python
  def now(self) -> datetime.datetime: ...
  def elapsed(self, since: datetime.datetime) -> datetime.timedelta: ...
  def tag(self) -> str: ...
  def names(self) -> list[str]: ...
  def lookup(self) -> dict[str, Point]: ...
  def maybe(self, value: Optional[int]) -> Optional[str]: ...
  def compute(self, input: Optional[list[Point]]) -> Optional[dict[str, int]]: ...
  ```
- `Coordinate.py`: `Point = Point` (typealias re-exports the underlying type; the redundant
  `from ...Point import Point` is harmless and keeps the import machinery uniform).
- `Callback.py`: `Callback = Callable[[int], None]` (lambda → `typing.Callable`).
- `pybind11/com_example_types_Calculator.cpp` includes `<pybind11/chrono.h>` (for Date/Duration).
- `pybind11/_return_caster.h` emitted with `#include <Return.h>` (correct for the no-internal-
  namespace case; becomes `<lorem_ipsum/Return.h>` when `-cppnamespace lorem_ipsum` is set).

### Caster syntax
- The caster header logic was syntax-checked against pybind11 + Python.h
  (`c++ -fsyntax-only`); the only errors are the expected "no member named 'Return' in global
  namespace" because the real generated `Return.h` is not present in the isolated test. The
  template itself is valid and was already proven to compile & run in the Phase 0 spike.

## Known limitations (later phases)
- The `Return` caster is emitted but **not yet `#include`d by the per-element `.cpp` files** — that
  happens in Phase 6 when the module init (`_module_init.cpp`) aggregates all `register_*` functions
  and includes `_return_caster.h`. Until then, functions returning `Return<T,Error>` (i.e. LIME
  functions with a `throws`/error) will not compile standalone.
- `Locale` maps to `str` (BCP-47 string) on the Python side; the C++ side uses the generated
  `Locale` type. A custom caster for `Locale` (plan §4.1) is **not** implemented — it currently
  relies on the C++ `Locale` being convertible to/from `std::string`, which is not automatic. This
  is a known gap to address if `Locale` is used across the boundary (tracked for Phase 5/6).
- No `.pyi` stubs yet (Phase 6).

## Next step
Phase 5 — Object Lifecycle and Callbacks: trampoline classes for interfaces (so Python can implement
them), referential-equality wrapper cache, GIL-safe callbacks, and exception translation wiring the
`Return` caster's failure path to the generated `Error` subclass.

## Smoke tests (separate doc)
The implemented features (Phases 1–4) are now covered by smoke tests — see
`docs/python_binding_dev/phase4_smoke_tests.md`. Summary: pybind11 output was nested under
`python/` so the `SmokeTest` harness discovers both `.py` and `.cpp` reference files; reference
output was generated for all existing smoke features that parse successfully, plus a dedicated
`python_attributes` feature exercising the `@Python(Name/Skip/Internal)` attribute. 43 python
smoke tests run, 5 skipped (pre-existing parse failures shared by all generators, and the
python-specific `name_clash_overloads` filename collision), 0 failed.
