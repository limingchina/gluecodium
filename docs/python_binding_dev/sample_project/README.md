# Gluecodium → Python (pybind11) Sample Project

This folder is a **minimal, runnable end-to-end example** of the Gluecodium
Python generator. It shows the full workflow:

1. Write an API in **LimeIDL** (`lime/Greeter.lime`).
2. Run **Gluecodium** to generate **C++ headers/impls + runtime** and
   **Python (pybind11) bindings** (`cpp/` + `python/`).
3. Provide the **C++ implementation** of the generated abstract classes
   (`cpp/GreeterImpl.cpp`).
4. Build a **CPython extension module** with **CMake** (the `PYBIND11_MODULE`
   entry point is generated for you — no hand-written `module.cpp` needed).
5. Use the API from **Python** (`python/client.py`).

The example models a small `Greeter` service with a `struct`, an `interface`
callback, a `throws` error, and a `property` — covering the main LIME features
the Python generator supports today.

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| JDK  | 17      | To build/run Gluecodium (`JAVA_HOME`). |
| CMake| ≥ 3.19  | Configures generation + builds the extension. |
| C++  | ≥ C++17 | Compiler with pybind11 support. |
| Python | ≥ 3.8 | With `pybind11` installed (`pip install pybind11`). |

You also need a **built Gluecodium distribution**. From the repository root:

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
./gradlew :gluecodium:installDist
```

This produces the CLI launcher at
`gluecodium/build/install/gluecodium/bin/gluecodium`.

---

## Project layout

```
sample_project/
├── CMakeLists.txt          # Drives Gluecodium generation + builds the .so
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

## Build & run

From this directory:

```bash
# 1. Configure. Point Gluecodium at the built CLI (or set GLUECODIUM_REPO).
cmake -S . -B build \
  -DGLUECODIUM_BIN=/path/to/gluecodium/build/install/gluecodium/bin/gluecodium \
  -DCMAKE_PREFIX_PATH="$(python3 -c 'import pybind11; print(pybind11.get_cmake_dir())')"

# 2. Build. This also runs Gluecodium to (re)generate the bindings.
cmake --build build

# 3. Run the client against the freshly built module.
cd build && python3 client.py
```

Expected output:

```
Created: <com.example.greeter.Greeter object at 0x...>
greet('World') -> Hello, World!
[listener] greeted: Ada
greeting_count -> 2
greeting_count after set -> 10
greet('') raised: RuntimeError - ::com::example::greeter::GreeterErrorCode::EMPTY_NAME
Greeting struct: Bob 3
```

---

## What the workflow does

### 1. LimeIDL input (`lime/Greeter.lime`)

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

### 2. Generation (driven by CMake)

`CMakeLists.txt` invokes the Gluecodium CLI:

```bash
gluecodium -input lime/Greeter.lime -output build/generated \
           -generators cpp,python -pythonmodule greeter
```

This produces, under `build/generated/`:

- `cpp/include/...` — C++ abstract classes + the Gluecodium **runtime headers**
  (`Return.h`, `ExportGluecodiumCpp.h`, `TypeRepository.h`, hash headers, …).
- `cpp/src/...` — generated C++ impl skeletons + runtime sources.
- `python/pybind11/*.cpp` — one `register_<Name>(py::module_&)` function per
  LIME type, plus the shared `_return_caster.h` / `_wrapper_cache.h` helpers and
  the `PYBIND11_MODULE` entry point (`_module_init.cpp`).
- `python/__init__.py` and `python/com/example/greeter/*.py` — thin Python
  wrapper classes (see the limitation note below).

### 3. C++ implementation (`cpp/GreeterImpl.cpp`)

Gluecodium generates **abstract** classes (`Greeter`, `GreetingListener`). The
application must implement them. `GreeterImpl.cpp` provides:

- the body of `Greeter::greet` / `add_listener` / the `greeting_count` property,
- the static `Greeter::create()` factory returning a `shared_ptr`,
- an out-of-line definition of the pure-virtual `GreetingListener::on_greeting`
  (the generated `GreetingListener` has no body, so this gives the trampoline's
  vtable a home; the Python-side override is what actually runs).

### 4. Python client (`python/client.py`)

The client imports the native extension module `greeter` and:

- creates a `Greeter` via `Greeter.create()`,
- calls `greet("World")` (returns a `str`),
- subclasses `GreetingListener` in Python and registers it — the C++ side
  invokes the override through a **GIL-safe trampoline**,
- reads/writes the `greeting_count` property,
- triggers the `throws GreeterError` path (mapped to a Python `RuntimeError`),
- builds a `Greeting` struct and reads its fields.

---

## Known limitations (Phase 6 of the Python generator)

The sample runs **without any hand-written pybind11 glue** — the generator emits the
`PYBIND11_MODULE` entry point, the `std::shared_ptr` holder for `class` types, and
`py::init<>()` for `struct`/`interface` types, and the CMake build (Phase 7) drives the
extension module through the `gluecodium_target_python_sources()` helper. The remaining
limitations are:

1. **`@Async`** functions are not yet bound (Phase 5.5, deferred).
2. The **wrapper cache** is generated but not yet wired into `return_value_policy`
   at call sites, so referential equality is not yet enforced.
3. The **`Locale`** caster is still missing.

The generated **Python wrapper classes** (`python/com/example/greeter/*.py`) are now
**directly importable and constructible**: each package directory gets an `__init__.py`,
the circular self-import is filtered out, and the wrappers expose factory constructors
(`Greeter.create()`, `Greeting(name, count)`, `GreetingListener()` subclassing). The
`python/client.py` therefore drives the generated wrappers directly.

The error raised on `greet("")` currently carries the qualified enum name
(`::com::example::greeter::GreeterErrorCode::EMPTY_NAME`) because the generated
`Return<std::error_code>` caster stringifies the `error_code` via its default
message; a custom `ReturnErrorToString` specialization can make this friendlier.
