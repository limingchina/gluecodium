# Sample Project — End-to-End Python (pybind11) Workflow

**Status**: ✅ Runnable (verified from a clean build)
**Branch**: `python_bind`
**Prerequisite**: Phases 0–5 of `docs/python_pybind11_plan.md` (the `python` generator
must be implemented through Phase 5, and a Gluecodium distribution must be built).
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

### 5.2 `cpp/module.cpp` (Phase 6 glue)

Gluecodium's `python` generator (currently at **Phase 5**) emits per-type `register_*`
functions but **not** the `PYBIND11_MODULE` aggregator. This file supplies it, calling the
generated `register_Greeting` / `register_GreeterErrorError` and providing corrected
bindings for the types that Phase 5 does not yet bind correctly (see §6).

Forward declarations in this file use `pybind11::module_&` (not `py::module_&`) because the
`py` alias is not in scope at that point.

---

## 6. Known limitations (Phase 6 of the Python generator)

The sample now runs **without any hand-written pybind11 glue**. The remaining limitations
are:

1. **`@Async`** functions are not yet bound (Phase 5.5, deferred).
2. The **wrapper cache** is generated but not yet wired into `return_value_policy` at call
   sites, so referential equality is not yet enforced.
3. The **`Locale`** caster is still missing.

The generated **Python wrapper classes** (`python/com/example/greeter/*.py`) are now
importable and the client drives the **native** pybind11 classes directly (the same
approach works against the generated `com.example.greeter.Greeter` Python class).

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
