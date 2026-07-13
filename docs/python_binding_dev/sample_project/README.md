# Gluecodium → Python (pybind11) Sample Project

This folder is a **minimal, runnable end-to-end example** of the Gluecodium
Python generator. It shows the full workflow:

1. Write an API in **LimeIDL** (`lime/Greeter.lime`).
2. Run **Gluecodium** to generate **C++ headers/impls + runtime** and
   **Python (pybind11) bindings** (`cpp/` + `python/`).
3. Provide the **C++ implementation** of the generated abstract classes and a
   **module entry point** (`cpp/GreeterImpl.cpp`, `cpp/module.cpp`).
4. Build a **CPython extension module** with **CMake**.
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
│   ├── GreeterImpl.cpp     # C++ implementation of the generated abstract classes
│   └── module.cpp          # PYBIND11_MODULE entry point (Phase 6 glue)
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
Created: <greeter.Greeter object at 0x...>
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
  LIME type, plus the shared `_return_caster.h` / `_wrapper_cache.h` helpers.
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

### 4. Module entry point (`cpp/module.cpp`)

Gluecodium's `python` generator (currently at **Phase 5**) emits per-type
`register_*` functions but **not** the `PYBIND11_MODULE` aggregator. This file
supplies it, calling the generated `register_Greeting` / `register_GreeterErrorError`
and providing corrected bindings for `Greeter` (with a `std::shared_ptr` holder)
and `GreetingListener` (with `py::init<>()`) so the module is actually runnable.

### 5. Python client (`python/client.py`)

The client imports the native extension module `greeter` and:

- creates a `Greeter` via `Greeter.create()`,
- calls `greet("World")` (returns a `str`),
- subclasses `GreetingListener` in Python and registers it — the C++ side
  invokes the override through a **GIL-safe trampoline**,
- reads/writes the `greeting_count` property,
- triggers the `throws GreeterError` path (mapped to a Python `RuntimeError`),
- builds a `Greeting` struct and reads its fields.

---

## Known limitations (Phase 5 of the Python generator)

This sample works around three gaps that are scheduled to be closed in
**Phase 6**:

1. **No `PYBIND11_MODULE` entry point** is generated — `cpp/module.cpp` provides it.
2. **`class` types lack a `std::shared_ptr` holder** in the generated binding,
   so `create()` (which returns `shared_ptr`) cannot convert to Python. The
   sample re-binds `Greeter` with the correct holder.
3. **`interface` types have no `py::init<>()`**, so Python subclasses cannot be
   instantiated as trampolines. The sample re-binds `GreetingListener` with
   `py::init<>()`.

Additionally, the generated **Python wrapper classes** (`python/com/example/
greeter/*.py`) currently have a circular self-import and no factory, so they are
not directly importable. The client therefore drives the **native** pybind11
classes directly. Once Phase 6 lands, the same client logic can be written
against the generated `com.example.greeter.Greeter` Python class instead.

The error raised on `greet("")` currently carries the qualified enum name
(`::com::example::greeter::GreeterErrorCode::EMPTY_NAME`) because the generated
`Return<std::error_code>` caster stringifies the `error_code` via its default
message; a custom `ReturnErrorToString` specialization can make this friendlier.
