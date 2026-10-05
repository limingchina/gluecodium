# Phase 3 — Template System (Implementation)

> **Status**: ✅ Completed (not yet committed)
> **Date**: 2026-07-12
> **Source plan**: `docs/python_pybind11_plan.md` (Phase 3, lines 222–290)
> **Build**: `gluecodium` compiles; `-generators python` produces valid Python + pybind11 output.

## Goal

Flesh out the Phase 2 skeleton templates so that each top-level LIME element (class, interface,
struct, enum, exception) generates a **real Python wrapper** (delegating to the native C++ object
via pybind11) and a **real pybind11 binding** (`register_<Name>(py::module_&)` function). Phase 2
only emitted empty-body stubs.

## Design

### Python side — thin wrapper
Each generated Python class holds `self._native` (the C++ object exposed by pybind11) and delegates
method/property access to it:

```python
class Calculator:
    def __init__(self, native):
        self._native = native

    def add(self, a: int, b: int) -> int:
        return self._native.add(a, b)

    @property
    def last_result(self) -> int:
        return self._native.last_result
```

### pybind11 side — `register_*` functions
Each element `.cpp` defines a free function `void register_<Name>(py::module_& module)` that binds
the type. The single `PYBIND11_MODULE` entry point (Phase 6) will call all `register_*` functions.
This matches the plan's file layout (`<module>_bindings.cpp` per element + `_module_init.cpp`).

```cpp
void register_Calculator(py::module_& module) {
    py::class_<Calculator>(module, "Calculator")
        .def("create", &Calculator::create)
        .def("add", &Calculator::add, py::arg("a"), py::arg("b"))
        .def_property("last_result", &Calculator::get_last_result);
}
```

## Templates added/changed

### Shared partials (new)
| Template | Purpose |
|----------|---------|
| `PythonFunction.mustache` | Python method body (delegates to `self._native`). |
| `PythonProperty.mustache` | Python `@property` + optional setter. |
| `PythonField.mustache` | Python struct field declaration. |
| `Pybind11Function.mustache` | `.def("name", &Class::method, py::arg(...))`. |
| `Pybind11Property.mustache` | `.def_property("name", &Class::get_x, &Class::set_x)`. |

### Per-type templates (filled in)
- `PythonClass` / `PythonInterface` — class with `__init__(native)` + functions + properties
  (interface inherits from parent classes via `parents`).
- `PythonStruct` — class with `__init__(native)` + fields + functions + properties.
- `PythonEnumeration` — `class X(Enum)` with ordinal values (`RED = 0`).
- `PythonException` — `class X(Exception)` with `message`.
- `Pybind11Class` / `Pybind11Interface` — `py::class_<>` binding with `register_*` wrapper.
- `Pybind11Struct` — `py::class_<>` with `.def_readwrite` for fields.
- `Pybind11Enum` — `py::enum_<>` with `.value("RED", Color::RED)`.
- `Pybind11Exception` — `py::exception<error_code>` registration.

### Common
- `Pybind11File.mustache` — now includes `<pybind11/stl.h>` (needed for STL type conversions).

### Unchanged from Phase 2
- `PythonFile`, `PythonInit`, `Pybind11File` skeleton, `PythonLambda`, `PythonTypeAlias`,
  `Pybind11Lambda`, `Pybind11TypeAlias` (lambdas/typealiases are minimal placeholders; full
  treatment is Phase 4/5).

## Key template mechanics
- **C++ names** resolved via the `"Pybind11"` resolver (wraps `CppNameResolver`):
  `{{resolveName model "Pybind11"}}` → C++ class type, `{{resolveName this "Pybind11"}}` → C++
  method/field/enumerator name, `{{resolveName this "Pybind11" "getter"}}` / `"setter"` → C++
  accessor names (uses the `resolveName` helper's sub-key support).
- **Python names** resolved via the default resolver: `{{resolveName}}` → Python name
  (honouring `@Python(Name=...)`), `{{resolveName typeRef}}` → Python type annotation.
- **Enum values**: ordinal `{{iter.position}}` for Python; `Enum::ENUMERATOR` for C++.
- **Properties**: `hasSetter` predicate drives whether a setter is emitted.

## Verification

### Compile-time
- `./gradlew :gluecodium:installDist` → success.

### Runtime (end-to-end)
Generated on `docs/python_binding_dev/phase2/test_python.lime` (enum/struct/interface/class/
exception), `-generators python` (no `-cppnamespace`, so C++ headers land at
`com/example/test/X.h` and includes are `com/example/test/X.h`):

- **All 5 `.py` files pass `python3 -m py_compile`** (syntactically valid).
- Sample `Calculator.cpp`:
  ```cpp
  #include <pybind11/pybind11.h>
  #include <pybind11/stl.h>
  #include "com/example/test/Calculator.h"

  void register_Calculator(py::module_& module) {
      py::class_<Calculator>(module, "Calculator")
          .def("create", &Calculator::create)
          .def("add", &Calculator::add, py::arg("a"), py::arg("b"))
          .def_property("last_result", &Calculator::get_last_result);
  }
  ```
- Enum: `RED = 0` (Python) / `Color::RED` (C++). Struct: `&Point::x` (correct C++ field).
- Interface: `py::class_<Listener, std::shared_ptr<Listener>>` (correct shared_ptr holder).

### Known limitations (addressed in later phases)
- **No `PYBIND11_MODULE` entry point yet** — the `register_*` functions need a module init
  (`_module_init.cpp`), which is Phase 6. The `.cpp` files are not yet independently compilable
  into an extension module.
- **No trampoline classes** for interface subclassing from Python (Phase 5).
- **No `Return<T,Error>` conversion** — functions returning errors currently bind the C++ method
  directly; the custom caster from the Phase 0 spike is wired in Phase 4.
- **No type stubs (`.pyi`)** yet (Phase 6).
- **Lambdas / type aliases** are still minimal placeholders.

## Next step
Phase 4 — Type mapping: wire the Phase 0 `Return<T,Error>` caster, Date/Duration casters, and
full basic/compound/user-defined type mapping into the resolvers + a `Pybind11TypeCaster`
template.
