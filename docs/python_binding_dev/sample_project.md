# Sample Project — End-to-End Python (pybind11) Workflow

**Status**: ✅ Runnable (verified from a clean build)
**Branch**: `python_bind`
**Prerequisite**: Phases 0–6 of `docs/python_pybind11_plan.md` (the `python` generator
must be implemented through Phase 6, and a Gluecodium distribution must be built). Phase 7
(the CMake integration) is also implemented, and this sample uses the
`gluecodium_target_python_sources()` helper it provides.
**Location**: `docs/python_binding_dev/sample_project/`

This document describes the **minimal, runnable end-to-end example** of the Gluecodium
Python generator. It is the companion write-up to the actual files in
`sample_project/`; the `sample_project/README.md` is the user-facing quick-start, while
this page records *why* the project is structured the way it is and *what* it verifies.

---

## 1. Purpose

The sample proves the full Python binding workflow works, not just that individual
generated files compile:

1. Write an API in **LimeIDL** (`lime/Greeter.lime`).
2. Run **Gluecodium** to generate **C++ headers/impls + runtime** and **Python (pybind11)
   bindings** (`cpp/` + `python/`).
3. Provide the **C++ implementation** of the generated abstract classes
   (`cpp/GreeterImpl.cpp`).
4. Build a **CPython extension module** with **CMake** (the `PYBIND11_MODULE` entry
   point is generated — no hand-written `module.cpp` is needed).
5. Use the API from **Python** (`python/client.py`).

It deliberately exercises the main LIME features the Python generator supports today:
a `struct`, an `interface` callback, a `throws` error, and a `property`.

---

## 2. Project layout

```
sample_project/
├── CMakeLists.txt          # Drives Gluecodium generation + builds the .so
├── README.md               # User-facing quick-start
├── .gitignore              # Excludes build/ and *.so
├── lime/
│   └── Greeter.lime        # The API definition (LimeIDL)
├── cpp/
│   └── GreeterImpl.cpp     # C++ implementation of the generated abstract classes
├── python/
│   └── client.py           # End-to-end Python client
└── build/                  # CMake build dir (generated)
    └── greeter*.so         # The built CPython extension module
```

---

## 3. The LimeIDL input

`lime/Greeter.lime` (package `com.example.greeter`):

```lime
package com.example.greeter

struct Greeting {
    name: String
    count: Int = 1
}

interface GreetingListener {
    fun onGreeting(value: String)
}

enum GreeterErrorCode { EMPTY_NAME }
exception GreeterError(GreeterErrorCode)

class Greeter {
    constructor create()
    fun greet(name: String): String throws GreeterError
    fun addListener(listener: GreetingListener)
    property greetingCount: Int
}
```

**Design notes / pitfalls that shaped this input:**

- **Comments use `#`, not `//`.** LimeIDL treats `//` as a syntax error
  (`mismatched input '//' expecting {NewLine, 'package'}`). All comments in the
  sample are `#`.
- **No `-cppnamespace` flag.** The C++ namespace is derived from the Lime `package`
  automatically. Passing `-cppnamespace com.example.greeter` *doubles* the namespace
  (`com/example/greeter/com/example/greeter`). The CMake invocation omits it.
- **`exception GreeterError(GreeterErrorCode)`, not `(String)`.** An enum error maps to
  `Return<Value, std::error_code>` (a supported path). A string error would map to
  `Return<string, string>`, whose constructors are ambiguous and fail to compile. Use an
  enum error type.

---

## 4. Generation (driven by CMake at configure time)

`CMakeLists.txt` locates the Gluecodium CLI (`GLUECODIUM_BIN` or `GLUECODIUM_REPO`) and
runs it **at CMake configure time** via `execute_process`:

```bash
gluecodium -input lime/Greeter.lime -output <build>/generated \
           -generators cpp,python -pythonmodule greeter
```

Generation happens at **configure time** (not as a build-time custom command) because
`python_add_library` validates its source list at configure time, and a `file(GLOB)` at
configure time would capture nothing if the files were generated later in the build. The
CMake file therefore uses **explicit source lists** for both the pybind11 bindings and the
C++ runtime/impl sources.

This produces, under `<build>/generated/`:

- `cpp/include/...` — C++ abstract classes + the Gluecodium **runtime headers**
  (`Return.h`, `ExportGluecodiumCpp.h`, `TypeRepository.h`, hash headers, `Locale.h`, …).
- `cpp/src/...` — generated C++ impl skeletons + runtime sources
  (`LocaleImpl.cpp`, `TypeRepositoryImpl.cpp`, `com/example/greeter/*.cpp`).
- `python/pybind11/*.cpp` — one `register_<Name>(py::module_&)` function per LIME type,
  plus the shared `_return_caster.h` / `_wrapper_cache.h` helpers and the generated
  `PYBIND11_MODULE` entry point (`_module_init.cpp`).
- `python/__init__.py` and `python/com/example/greeter/*.py` — thin Python wrapper classes
  (see the limitation note in §6).

The C++ runtime headers are emitted by the `cpp` generator's common output, so the sample
always generates `cpp,python` together.

---

## 5. C++ implementation and module entry point

### 5.1 `cpp/GreeterImpl.cpp`

Gluecodium generates **abstract** classes (`Greeter`, `GreetingListener`). The application
must implement them. `GreeterImpl.cpp` provides:

- the body of `Greeter::greet` / `add_listener` / the `greeting_count` property,
- the static `Greeter::create()` factory returning a `shared_ptr`,
- an out-of-line definition of the pure-virtual `GreetingListener::on_greeting`
  (the generated `GreetingListener` has no body, so this gives the trampoline's vtable a
  home; the Python-side override is what actually runs).

**Linkage pitfall (resolved):** the generated `Greeter.cpp` / `GreetingListener.cpp`
*already* define the destructors (and therefore emit the vtable/typeinfo). An earlier
version of `GreeterImpl.cpp` also defined `~Greeter()` / `~GreetingListener()` out-of-line,
causing 12 duplicate-symbol link errors. The fix was to remove those duplicate destructor
definitions and keep only `on_greeting` (which has no body in the generated code).

### 5.2 Building the extension module (Phase 7 glue)

The `python` generator emits the per-type `register_*` functions **and** the
`PYBIND11_MODULE` aggregator (`_module_init.cpp`), so **no hand-written `module.cpp` is
needed**. The CMake build drives the extension module through the
`gluecodium_target_python_sources()` helper (provided by `cmake/modules/gluecodium/Python.cmake`,
included via `Gluecodium.cmake`):

```cmake
add_library(greeter_cpp STATIC ${CPP_SOURCES} cpp/GreeterImpl.cpp)
gluecodium_target_python_sources(greeter_cpp
  MODULE_NAME "${PY_MODULE}"          # "greeter" -> PYBIND11_MODULE(greeter, m)
  OUTPUT_DIR "${GEN_OUTPUT}"          # dir that contains python/pybind11/*.cpp
  OUTPUT greeter_python)              # module target name (greeter_cpp_python)
```

The helper globs `python/pybind11/*.cpp`, creates a `python_add_library(... MODULE
WITH_SOABI)` target linked to `greeter_cpp`, and sets the module target's `OUTPUT_NAME` to
the module name so the built `.so`/`.pyd` filename matches the `PYBIND11_MODULE` symbol
(Python imports by filename). When generation goes through `gluecodium_generate` instead of
a manual `execute_process`, the `OUTPUT_DIR` argument can be omitted (it is read from the
target's `GLUECODIUM_OUTPUT_UNITY_DIR` property).

---

## 6. Known limitations (Phase 6 of the Python generator)

The sample runs **without any hand-written pybind11 glue** — the generator emits the
`PYBIND11_MODULE` entry point, the `std::shared_ptr` holder for `class` types, and
`py::init<>()` for `struct`/`interface` types, and Phase 7 builds it through the CMake
helper. The remaining limitations are:

1. **`@Async`** functions are not yet bound (Phase 5.5, deferred).
2. The **wrapper cache** is generated but not yet wired into `return_value_policy` at call
   sites, so referential equality is not yet enforced.
3. The **`Locale`** caster is still missing.

The generated **Python wrapper classes** (`python/com/example/greeter/*.py`) currently have
a circular self-import and no factory, so they are not directly importable. The client
therefore drives the **native** pybind11 classes directly. Once that is fixed, the same
client logic can be written against the generated `com.example.greeter.Greeter` Python
class instead.

The error raised on `greet("")` currently carries the qualified enum name
(`::com::example::greeter::GreeterErrorCode::EMPTY_NAME`) because the generated
`Return<std::error_code>` caster stringifies the `error_code` via its default message; a
custom `ReturnErrorToString` specialization can make this friendlier.

---

## 7. Build & run

From `docs/python_binding_dev/sample_project/`:

```bash
# 0. Build Gluecodium once (from the repo root).
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
./gradlew :gluecodium:installDist

# 1. Configure. Point Gluecodium at the built CLI (or set GLUECODIUM_REPO).
cmake -S . -B build \
  -DGLUECODIUM_BIN=/path/to/gluecodium/build/install/gluecodium/bin/gluecodium \
  -DCMAKE_PREFIX_PATH="$(python3 -c 'import pybind11; print(pybind11.get_cmake_dir())')"

# 2. Build (also (re)generates the bindings at configure time).
cmake --build build

# 3. Run the client against the freshly built module.
cd build && python3 client.py
```

To regenerate after editing `lime/Greeter.lime`, re-run `cmake -S . -B build` (configure
time is when generation happens), then `cmake --build build`.

---

## 8. Verification (clean build)

A from-scratch `rm -rf build && cmake -S . -B build ... && cmake --build build` followed by
`python3 client.py` produces:

```
Created: <greeter.Greeter object at 0x...>
greet('World') -> Hello, World!
[listener] greeted: Ada
greeting_count -> 2
greeting_count after set -> 10
greet('') raised: RuntimeError - ::com::example::greeter::GreeterErrorCode::EMPTY_NAME
Greeting struct: Bob 3
```

This confirms: object creation, method calls returning `str`, GIL-safe C++ → Python
callbacks through a trampoline, property read/write, `throws` error mapping to
`RuntimeError`, and `struct` construction — i.e. the full Phase 5 feature set exercised
end-to-end.
