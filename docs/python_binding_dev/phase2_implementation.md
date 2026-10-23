# Phase 2 — Generator Skeleton (Implementation)

> **Status**: ✅ Completed (not yet committed)
> **Date**: 2026-07-12
> **Source plan**: `docs/python_pybind11_plan.md` (Phase 2, lines 120–218)
> **Build**: `lime-runtime`, `gluecodium` compile with openjdk 17; generator runs end-to-end.

## Goal

Create the Python generator package (`PythonGenerator` + supporting resolvers/predicates/
validators), register it with the `ServiceLoader`, and add the minimal Mustache templates so
that `-generators python` produces both Python source files and pybind11 C++ binding files for a
LIME model. Full type mapping, lifecycle, and output structure are later phases.

## Design decision: modeled after the **Swift** generator, not Dart

The plan suggested modeling after `DartGenerator`, but the **Swift generator is a much closer
architectural match** for pybind11:

| Aspect | Dart (FFI) | Swift (CBridge) | **Python (pybind11)** |
|--------|-----------|-----------------|------------------------|
| Platform output | Dart | Swift | **Python** |
| C++ binding output | FFI C++ (C-ABI shim) | CBridge C++ (wraps C++ API directly) | **pybind11 C++ (wraps C++ API directly)** |
| Intermediate C-ABI layer? | Yes | No | **No** |
| Reuses `CppNameResolver`/`CppIncludeResolver`? | No (own FFI resolvers) | Yes | **Yes** |

Both Swift and Python generate *platform code + C++ binding code that `#include`s the generated
C++ headers and calls the C++ API directly*. So `PythonGenerator` follows the Swift structure:
filter the model with `LimeModelSkipPredicates` (PYTHON attribute), build a `PythonNameResolver`
for platform names, a `Pybind11NameResolver` (wrapping `CppNameResolver`) for C++ names, run
validators, then emit `.py` and `.cpp` files via templates.

## Changes

### 2.1–2.2 Generator package — `gluecodium/.../generator/python/`

| File | Purpose |
|------|---------|
| `PythonGenerator.kt` | Main generator. `shortName = "python"`. Filters model, builds resolvers, runs `PythonOverloadsValidator`, renders `python/PythonFile` + `python/Pybind11File` templates, emits `__init__.py`. |
| `PythonNameResolver.kt` | LIME → Python name resolution (basic types → Python types, `@Python(Name=...)` override, comments). |
| `Pybind11NameResolver.kt` | LIME → C++ name resolution for binding code; wraps `CppNameResolver` with `forceFollowThrough`. |
| `PythonImportResolver.kt` | Resolves Python `import`/`from ... import` statements; skips basic types, honors external `importPath`. |
| `PythonImportsCollector.kt` | Collects Python imports for an element + nested declarations (`GenericImportsCollector`). |
| `Pybind11IncludeResolver.kt` | C++ `#include` resolution for binding code; delegates to `CppIncludeResolver`. |
| `PythonGeneratorPredicates.kt` | Template `ifPredicate`/`unlessPredicate` helpers (`isInternal`, `isPublic`, `isOverloaded`, `needsAllFieldsConstructor`, …). |
| `PythonCommentsProcessor.kt` | Markdown → Python docstring comment processing. |
| `PythonOverloadsValidator.kt` | Rejects overloaded method names (Python has no overloading). |
| `Pybind11Helpers.kt` | Pure helpers for binding templates (trampoline detection, internal check). |
| `PythonImport.kt` | `data class` for a Python import (`modulePath`, `importedName`). |
| `PythonNameRules.kt` | File-name + platform-name rules; honors `@Python(Name=...)`. |
| `package-info.java` | Package documentation. |

### 2.3 Registration — `META-INF/services/...Generator`

Added `com.here.gluecodium.generator.python.PythonGenerator` to the `ServiceLoader` manifest so
`-generators python` discovers it.

### 2.4 Templates — `gluecodium/.../resources/templates/python/`

Minimal but valid Mustache templates (skeleton; bodies filled in later phases):

- `PythonFile.mustache` — Python file skeleton (imports + `{{include contentTemplate}}`).
- `PythonInit.mustache` — package `__init__.py`.
- `Pybind11File.mustache` — pybind11 `.cpp` skeleton (`#include <pybind11/pybind11.h>` + includes + `{{include contentTemplate}}`).
- Per-type: `Python{Class,Interface,Struct,Enumeration,Exception,Lambda,TypeAlias}.mustache`
  and `Pybind11{Class,Interface,Struct,Enum,Exception,Lambda,TypeAlias}.mustache`.

### Supporting changes

- `GeneratorOptions.kt`: added `WARNING_PYTHON_OVERLOADS = "PythonOverloads"` constant (used by
  `PythonOverloadsValidator` via `options.werror`).
- `LimeExternalDescriptor.kt` (`lime-runtime`): added `python` property + `PYTHON_TAG = "python"`
  + `getFor(PYTHON)` branch, so `@Python(external ...)` descriptors resolve (needed by
  `PythonImportResolver` for external types).
- `namerules/python.properties`: corrected format values to `lower_snake_case` (the konfig
  `NameFormat` enum rejects bare `snake_case`).

## Verification

### Compile-time
- `./gradlew :lime-runtime:compileKotlin :gluecodium:compileKotlin` → **success**.

### Runtime (end-to-end)
Built the distribution and ran on `docs/python_binding_dev/phase2/test_python.lime`
(enum / struct / interface / class / exception):

```
./gluecodium -input .../test_python.lime -output /tmp/python_out3 \
    -generators python -cppnamespace com.example.test
# exit 0, 11 files generated
```

Generated layout:
```
python/
├── __init__.py
└── com/example/test/{Calculator,Color,Listener,MyErrorError,Point}.py
pybind11/
└── com_example_test_{Calculator,Color,Listener,MyErrorError,Point}.cpp
```

Sample `python/com/example/test/Calculator.py`:
```python
from com.example.test.Calculator import Calculator

class Calculator:
    """"""

    def __init__(self, native):
        self._native = native
```

Sample `pybind11/com_example_test_Calculator.cpp`:
```cpp
#include <pybind11/pybind11.h>
#include "com/example/test/Calculator.h"
#include "cstdint"
#include "memory"

{
    py::class_<Calculator>(module, "Calculator")
        ;
}
```

The `@Python(Skip)` / `@Python(Internal)` / `@Python(Name=...)` filtering is wired through
`LimeModelSkipPredicates` + `PythonGeneratorPredicates.isInternal`/`isPublic` and will be
exercised once the templates emit real bodies (Phase 3+).

## Test fixture
`docs/python_binding_dev/phase2/test_python.lime` — minimal LIME covering all top-level element
kinds, kept for later-phase verification.

## Notes / deviations from plan

- **Modeled after Swift, not Dart** (see Design decision above). The plan's §2.1 file list is
  followed; `Pybind11Helpers.kt` is kept (plan lists it) though currently minimal.
- **Templates are skeletons**: they emit valid (but empty-body) Python/pybind11 files. Real
  method/property/field/constructor binding happens in Phase 3 (templates) and Phase 4 (type
  mapping).
- **`pythonModule`** defaults to `"generated"` (from Phase 1 `GeneratorOptions`); the module name
  is threaded into `__init__.py` and is the intended `PYBIND11_MODULE` name (wired in Phase 3).
- The `Pybind11NameResolver.resolveFullName` / `Pybind11Helpers` helpers are in place for Phase 3
  trampoline/class binding work.

## Next step

Phase 3 — Template system: flesh out the per-type templates (real method/property/constructor
bodies, `PYBIND11_MODULE` entry point, type stubs) and Phase 4 — type mapping (basic/compound/
user-defined types, `Return<T,Error>` caster from the Phase 0 spike).
