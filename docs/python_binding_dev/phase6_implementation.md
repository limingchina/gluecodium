# Phase 6 — Output File Structure (Implementation)

**Status**: ✅ Implemented
**Branch**: `python_bind`
**Prerequisite**: Phases 0–5 (the `python` generator through Phase 5 must be committed).

This document records the concrete changes made to implement Phase 6 of
`docs/python_pybind11_plan.md`: the generated output file layout — a `PYBIND11_MODULE`
entry point that aggregates the per-type `register_*` functions, Python type-stub (`.pyi`)
files, and the common Python build/helper files (`setup.py`, `pyproject.toml`,
`_native_base.py`).

---

## 1. What was implemented

| Plan item | Status | Notes |
|-----------|--------|-------|
| 6.1 Module init (`PYBIND11_MODULE`) | ✅ | `python/pybind11/_module_init.cpp` aggregates every per-type `register_<Name>(py::module_&)`. |
| 6.1 `.pyi` type stubs | ✅ | One `<Name>.pyi` per top-level LIME element, mirroring the `.py` wrappers. |
| 6.1 `setup.py` / `pyproject.toml` | ✅ | PEP 518 build config + `pybind11.setup_helpers.Pybind11Extension` over `pybind11/*.cpp`. |
| 6.1 `_native_base.py` | ✅ | Shared `_NativeBase` base class; class/interface/struct wrappers now extend it. |
| 6.2 Build artifacts | ⬜ | The actual `.so`/`.pyd` build is driven by CMake (Phase 7) / functional tests (Phase 8). |

---

## 2. Files changed

### Kotlin (`gluecodium/src/main/java/.../generator/python/`)

- **`PythonNameRules.kt`**
  - Added `getPythonStubFileName(limeElement)` → `python/<pkg>/<Name>.pyi`.
  - Added `MODULE_INIT_FILE = pybind11/_module_init.cpp` companion constant.

- **`PythonGenerator.kt`**
  - `generatePythonFile` now returns **two** files: the `.py` wrapper and its `.pyi` stub
    (both rendered from the same template data, via `python/PythonFile` and `python/PythonStub`).
  - `generateCommonFiles` now additionally emits:
    - `pybind11/_module_init.cpp` — built from `python/Pybind11ModuleInit`, with a
      `registerFunctions` list derived from `pybind11FilteredModel.topElements`
      (excluding `LimeTypeAlias` and `LimeLambda`, which emit no binding).
    - `python/setup.py` (`python/PythonSetupPy`).
    - `python/pyproject.toml` (`python/PythonPyproject`).
    - `python/_native_base.py` (`python/PythonNativeBase`).
  - `generateCommonFiles` now takes the `pybind11FilteredModel` as a parameter (so the
    register-function list can be computed there).

### Templates (`gluecodium/src/main/resources/templates/python/`)

**New:**
- `Pybind11ModuleInit.mustache` — forward-declares each `register_<Name>`, then
  `PYBIND11_MODULE(<moduleName>, m)` calling them in sorted order. Includes
  `_wrapper_cache.h` + `_return_caster.h` so the whole module compiles standalone.
- `PythonStub.mustache` — stub skeleton (imports + `{{#model}}{{include contentTemplate}}`),
  mirroring `PythonFile.mustache`.
- `PythonStubClass.mustache`, `PythonStubInterface.mustache`, `PythonStubStruct.mustache`,
  `PythonStubEnumeration.mustache`, `PythonStubException.mustache`, `PythonStubLambda.mustache`,
  `PythonStubTypeAlias.mustache` — stub bodies (signatures only, `...` bodies).
- `PythonStubFunction.mustache`, `PythonStubProperty.mustache`, `PythonStubField.mustache` —
  stub partials mirroring the runtime partials (`PythonFunction`/`PythonProperty`/`PythonField`).
- `PythonSetupPy.mustache`, `PythonPyproject.mustache`, `PythonNativeBase.mustache` — common files.

**Modified:**
- `PythonClass.mustache`, `PythonInterface.mustache`, `PythonStruct.mustache` — now
  `from _native_base import _NativeBase` and extend `_NativeBase`, calling
  `super().__init__(native)` instead of `self._native = native`.

---

## 3. Generated output layout

```
python/
├── __init__.py
├── _native_base.py
├── setup.py
├── pyproject.toml
├── <package>/.../<Name>.py        # Python wrapper
├── <package>/.../<Name>.pyi       # type stub
└── pybind11/
    ├── _module_init.cpp           # PYBIND11_MODULE entry point
    ├── _return_caster.h
    ├── _wrapper_cache.h
    └── <pkg>_<Name>.cpp           # per-type register_* (from earlier phases)
```

The `.pyi` stub is a type-only companion: it carries the same class/function/property
signatures (with `...` bodies) so editors and `mypy` can type-check callers. It does **not**
import `_native_base` (stubs describe the public surface; the runtime `.py` provides the
implementation and the base-class relationship).

---

## 4. Verification

- `./gradlew :gluecodium:installDist` → success.
- `./gradlew :gluecodium:test` → **all tests pass** (SmokeTest: python 43 run / 5 skipped /
  0 failed; `name_clash_overloads` remains skipped — see the note below).
- Reference output for every python smoke feature was regenerated with the harness options
  (`-intnamespace gluecodium -internalprefix foobar_`, honouring each feature's
  `commandlineoptions.txt`).
- Spot-checked output:
  - `basic_types/output/python/pybind11/_module_init.cpp` forwards `register_BasicTypes` etc.
    and defines `PYBIND11_MODULE(generated, m)`.
  - `python_attributes/output/python/com/example/test/RenamedClass.pyi` honours the
    `@Python(Name = "RenamedClass")` rename (stub matches the `.py`).
  - `BasicTypes.py` now `class BasicTypes(_NativeBase)` with `super().__init__(native)`.

### 4.1 Smoke-test regeneration pitfall: `name_clash_overloads`

When regenerating the python smoke references with a bulk script (e.g. the loop in
`docs/python_binding_dev/phase4_smoke_tests.md`), the `name_clash_overloads` feature will
**appear** to generate python output, because two of its LIME types resolve to the same
Python file name `AssetsManager.py` and the generator throws a filename-collision error
(`checkForFileNameCollisions`). The bulk loop then commits that output, which makes the
`SmokeTest` case for `python` **fail** (`executeGenerator` returns false → `assertTrue`
fails) on the next run.

**This is a known, expected skip — do NOT commit python output for `name_clash_overloads`.**
The harness treats a feature as skipped for a generator when its `output/<generator>/`
directory has no reference files, so the correct state is:

```
gluecodium/src/test/resources/smoke/name_clash_overloads/output/
├── cpp/
└── (no python/ directory)
```

If a regeneration pass creates `name_clash_overloads/output/python/`, delete it before
committing:

```bash
rm -rf gluecodium/src/test/resources/smoke/name_clash_overloads/output/python
```

The other four skipped python features (`comments`, `generic_types`, `strict_fail_immutable`,
`strict_fail_internal`) are skipped for reasons unrelated to the python generator (parse
failures / intentional validation failures) and also have no `output/python/` directory.

---

## 5. Known limitations

- The `.so`/`.pyd` build artifact (plan §6.2) is **not** produced by the generator — it is the
  responsibility of the CMake integration (Phase 7) and the functional-test harness (Phase 8).
  The generated `setup.py`/`pyproject.toml`/`_module_init.cpp` are the inputs those builds consume.
- `@Async` (Phase 5.5) is still unimplemented; its absence is unchanged by this phase.
- The wrapper cache is generated but not yet wired into `return_value_policy` at call sites
  (referential equality not yet enforced) — unchanged from Phase 5.
- `Locale` caster still missing — unchanged from Phase 4/5.
