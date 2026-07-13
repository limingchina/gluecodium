# Phase 7 — CMake Integration (Implementation)

**Status**: ✅ Implemented
**Branch**: `python_bind`
**Prerequisite**: Phases 0–6 (the `python` generator through Phase 6 must be committed, so
that `python/pybind11/*.cpp` + `_module_init.cpp` are emitted).

This document records the concrete changes made to implement Phase 7 of
`docs/python_pybind11_plan.md`: wiring the Python generator into Gluecodium's CMake
toolchain so that C++ projects using Gluecodium via CMake can generate *and* compile the
Python (pybind11) bindings automatically.

---

## 1. What was implemented

| Plan item | Status | Notes |
|-----------|--------|-------|
| 7.1 Python target properties | ✅ | Four `GLUECODIUM_PYTHON_*` properties added to `KnownOptionalProperties.cmake`. |
| 7.2 Generated-files list | ⬜ (N/A) | The plan assumed a single "unity" file per generator (like `dart_..._ffiglue.cpp`). The `python` generator instead emits a **directory** of files (`python/pybind11/*.cpp` + common headers + `_module_init.cpp`), so there is no single unity file to register. The helper globs the directory instead (see §2). |
| 7.3 Supported generators list | ✅ | `python` added to `GLUECODIUM_SUPPORTED_GENERATORS`; auto-detected in `get_supported_gluecodium_generators.cmake` when `python3` **and** `pybind11` are found. |
| 7.4 pybind11 CMake integration | ✅ | New `Python.cmake` with `gluecodium_target_python_sources()`. |

---

## 2. Files changed

### CMake modules (`cmake/modules/gluecodium/`)

- **`gluecodium/KnownOptionalProperties.cmake`**
  - Added four target properties (mirroring the Dart/Kotlin pattern):
    - `GLUECODIUM_PYTHON_PACKAGE` — base Python package for generated sources.
    - `GLUECODIUM_PYTHON_INTERNAL_PACKAGE` — sub-package for internal Python code.
    - `GLUECODIUM_PYTHON_MODULE_NAME` — name of the generated `PYBIND11_MODULE`.
    - `GLUECODIUM_PYTHON_NAMERULES` — path to a Python name-rules file.

- **`gluecodium/details/ReadRequiredProperties.cmake`**
  - Added `python` to `GLUECODIUM_SUPPORTED_GENERATORS` (now `cpp android android-kotlin swift dart python`).

- **`gluecodium/details/runGenerate.cmake`**
  - Appended the four Python options to the Gluecodium options file so they reach the
    generator: `pythonpackage`, `pythonintpackage`, `pythonmodule`, `pythonnamerules`.

- **`tests/utils/get_supported_gluecodium_generators.cmake`**
  - `python` is now reported as supported when both `python3` (via `find_program`) and
    `pybind11` (via `find_package`) are available.

- **`Python.cmake`** (new)
  - Provides `gluecodium_target_python_sources(<target> [MODULE_NAME <name>]
    [OUTPUT_DIR <dir>] [OUTPUT <module_target>])`.
  - Locates `Python` (`Development.Module`) and `pybind11`, globs
    `<dir>/python/pybind11/*.cpp`, and creates a `python_add_library(<target>_python
    MODULE WITH_SOABI ...)` extension module linked to `<target>`.
  - Sets the module target's `OUTPUT_NAME` to the module name so the built `.so`/`.pyd`
    filename matches the `PYBIND11_MODULE` symbol (Python imports by filename).
  - `OUTPUT_DIR` is required when `<target>` was generated manually (e.g. via
    `execute_process`); otherwise it is read from the target's `GLUECODIUM_OUTPUT_UNITY_DIR`
    property set by `gluecodium_generate`.

- **`Gluecodium.cmake`** / **`All.cmake`**
  - `include(.../Python.cmake)` so the helper is available wherever the Gluecodium module
    is loaded.

### Sample project (`docs/python_binding_dev/sample_project/`)

- **`CMakeLists.txt`**
  - Replaced the hand-rolled `python_add_library(greeter ...)` + explicit source list with
    `gluecodium_target_python_sources(greeter_cpp MODULE_NAME "${PY_MODULE}"
    OUTPUT_DIR "${GEN_OUTPUT}" OUTPUT greeter_python)`.
  - The host C++ library is now a `STATIC` `greeter_cpp` target (generated runtime/impl +
    hand-written `GreeterImpl.cpp`); the helper links it into the extension module.
  - Includes `cmake/modules/gluecodium/Gluecodium.cmake` (resolving the module dir via
    `GLUECODIUM_REPO` or a relative path).

---

## 3. Design note: directory output vs. unity file

The Phase 7 plan (§7.2) was written assuming the Python generator would emit a single
"unity" source file, like the Dart generator's `dart/<name>_<group>_ffiglue.cpp`. In
reality the `python` generator (Phases 3–6) emits a **directory** of files:

```
<output>/python/pybind11/
├── _module_init.cpp        # PYBIND11_MODULE entry point
├── _return_caster.h
├── _wrapper_cache.h
└── <pkg>_<Name>.cpp        # one register_<Name>(py::module_&) per top-level LIME type
```

There is therefore no single unity file to register in `ListGeneratedFiles.cmake`. The
`gluecodium_target_python_sources()` helper instead **globs** `python/pybind11/*.cpp`, which
keeps the source list in sync with the LimeIDL input without manual maintenance. This is
safe because the sample generates at *configure* time (the glob captures the files before
`python_add_library` is configured); for the `gluecodium_generate` flow the glob runs on a
re-configure after the first build has populated the directory.

---

## 4. Verification

- `cmake -S . -B build -DGLUECODIUM_BIN=<cli> -DCMAKE_PREFIX_PATH=<pybind11 cmake dir>`
  configures cleanly (no "Unknown command" / missing-property errors).
- `cmake --build build` compiles `greeter_cpp` (host lib) and `greeter_cpp_python`
  (extension module), producing `greeter.cpython-312-darwin.so`.
- `cd build && python3 client.py` runs the end-to-end client and prints the expected
  output (greet, listener callback, property get/set, error path, struct).

---

## 5. Remaining work (out of scope for Phase 7)

- **`ListGeneratedFiles.cmake`**: not extended, because the Python output is a directory,
  not a unity file. If a future change makes the generator emit a single unity file, add
  the `python` branch there (mirroring the `dart` branch) and drop the glob in the helper.
- **Functional tests (Phase 8)**: the `functional-tests/functional/python/` suite and
  `build-python-functional` script are still to be added; they will consume this helper.
