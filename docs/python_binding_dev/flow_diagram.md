# Gluecodium Python Binding Pipeline

This document diagrams the full lifecycle of a Python binding built with Gluecodium:
from a **LimeIDL** source file, through **code generation**, **compilation** into native
libraries, the **Python bindings** those libraries produce, and finally **application**
usage. Every node maps to a concrete file from the
[`sample_project`](sample_project/) (`com.example.greeter`).

---

## 1. High-Level Pipeline

![High-level pipeline](flow_diagram_1.png)

<details><summary>Editable Mermaid source</summary>

```mermaid
flowchart TD
    LIME(["lime/Greeter.lime<br/>LimeIDL API definition"]):::source
    CPPIMPL(["cpp/GreeterImpl.cpp<br/>Hand-written C++ implementation"]):::source
    PYAPP(["python/client.py<br/>Application code"]):::source

    GC["Gluecodium CLI<br/><i>Java / Gradle tool</i><br/>-generators cpp,python"]:::tool

    subgraph G["Generated files  (build/generated/)"]
        direction LR
        GCPP["cpp/include/*.h  +  cpp/src/*.cpp<br/>C++ abstract classes + runtime"]:::gen
        GPYW["python/com/.../*.py  +  *.pyi<br/>Python wrappers + stubs"]:::gen
        GPYB["python/pybind11/*.cpp + *.h<br/>pybind11 C++ binding sources"]:::gen
    end

    subgraph B["CMake build  (compiler + linker)"]
        direction TB
        BLIB["add_library greeter_cpp STATIC<br/>generated cpp + runtime + GreeterImpl.cpp"]:::build
        BEXT["pybind11_add_module greeter_python<br/>globs pybind11/*.cpp, links greeter_cpp"]:::build
    end

    subgraph A["Built artifacts"]
        direction LR
        LIB["libgreeter_cpp.a<br/>C++ library"]:::artifact
        SO["greeter.cpython-3XX-platform.so<br/>CPython extension module"]:::artifact
    end

    subgraph P["Python bindings  (installed together)"]
        direction LR
        NAT["Native .so<br/>pybind11 <-> C++"]:::binding
        WRP[".py wrapper package<br/>com/example/greeter/*.py"]:::binding
    end

    APP["Application<br/>from com.example.greeter.Greeter import Greeter<br/>Greeter.create().greet('World')"]:::app

    LIME --> GC
    GC --> GCPP
    GC --> GPYW
    GC --> GPYB

    GCPP --> BLIB
    CPPIMPL --> BLIB
    GPYB --> BEXT
    BLIB -->|"link"| BEXT

    BLIB --> LIB
    BEXT --> SO

    SO --> NAT
    GPYW --> WRP

    NAT --> APP
    WRP --> APP
    PYAPP --> APP

    classDef source fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#78350f
    classDef tool fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a8a
    classDef gen fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef build fill:#f3e8ff,stroke:#9333ea,stroke-width:2px,color:#581c87
    classDef artifact fill:#ffedd5,stroke:#ea580c,stroke-width:2px,color:#7c2d12
    classDef binding fill:#cffafe,stroke:#0891b2,stroke-width:2px,color:#164e63
    classDef app fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#7f1d1d
```

</details>

---

## 2. Detailed File-Level Flow

This diagram traces every concrete file through the pipeline, using the
`com.example.greeter` sample.

![Detailed file-level flow](flow_diagram_2.png)

<details><summary>Editable Mermaid source</summary>

```mermaid
flowchart TD
    %% ---- Source ----
    LIME["lime/Greeter.lime<br/>================================<br/>package com.example.greeter<br/>struct Greeting<br/>interface GreetingListener<br/>enum GreeterErrorCode<br/>exception GreeterError<br/>class Greeter"]:::source
    IMPL["cpp/GreeterImpl.cpp<br/>bodies of greet / addListener<br/>Greeter::create() factory<br/>GreetingListener::on_greeting def"]:::source

    %% ---- Gluecodium internals ----
    subgraph GC["Gluecodium  (lime-loader + gluecodium)"]
        direction TB
        ANTLR["ANTLR grammar LimeIDL.g4<br/>-> parse tree"]:::tool
        LMODEL["LIME Model<br/>LimeType tree (lime-runtime)"]:::tool
        VAL["Validators<br/>type refs, inheritance, overloads..."]:::tool
        RESOLVE["Name Resolvers + Import Resolvers<br/>PythonNameRules, Pybind11NameResolver"]:::tool
        TMPL["Mustache templates (Trimou engine)<br/>templates/cpp/*  +  templates/python/*"]:::tool
    end

    LIME --> ANTLR --> LMODEL --> VAL --> RESOLVE --> TMPL

    %% ---- Generated: C++ ----
    subgraph GCPP["Generated C++  (cpp generator)"]
        direction TB
        HABS["cpp/include/com/example/greeter/<br/>Greeter.h  (abstract class)<br/>Greeting.h  (struct)<br/>GreetingListener.h  (pure virtual)<br/>GreeterErrorCode.h  (enum)"]:::gen
        HRT["cpp/include/<br/>Return.h, Hash.h, TypeRepository.h,<br/>Locale.h, VectorHash.h ...  (runtime)"]:::gen
        SRCGEN["cpp/src/com/example/greeter/<br/>Greeter.cpp, Greeting.cpp,<br/>GreetingListener.cpp, GreeterErrorCode.cpp<br/>(impl skeletons)"]:::gen
        SRCRT["cpp/src/<br/>LocaleImpl.cpp, TypeRepositoryImpl.cpp<br/>(runtime impl)"]:::gen
    end

    %% ---- Generated: Python wrappers ----
    subgraph GPYW["Generated Python wrappers  (python generator)"]
        direction TB
        PYW["python/com/example/greeter/<br/>Greeter.py + Greeter.pyi<br/>Greeting.py + Greeting.pyi<br/>GreetingListener.py + .pyi<br/>GreeterErrorCode.py + .pyi<br/>GreeterErrorError.py + .pyi"]:::gen
        PYBASE["python/<br/>__init__.py, _native_base.py,<br/>setup.py, pyproject.toml"]:::gen
    end

    %% ---- Generated: pybind11 ----
    subgraph GPYB["Generated pybind11 sources  (python generator)"]
        direction TB
        PBINIT["python/pybind11/_module_init.cpp<br/>PYBIND11_MODULE(greeter, m) entry point<br/>calls every register_* function"]:::gen
        PBREG["python/pybind11/<br/>com_example_greeter_Greeter.cpp<br/>com_example_greeter_Greeting.cpp<br/>com_example_greeter_GreetingListener.cpp<br/>com_example_greeter_GreeterErrorCode.cpp<br/>(register_Name(py::module_&) per type)"]:::gen
        PBHDR["python/pybind11/<br/>_return_caster.h  (Return&lt;T,Error&gt; -> Python)<br/>_wrapper_cache.h  (identity preservation)"]:::gen
    end

    TMPL --> GCPP
    TMPL --> GPYW
    TMPL --> GPYB

    %% ---- CMake build ----
    subgraph CMAKE["CMake build  (Gluecodium.cmake + Python.cmake)"]
        direction TB
        CMK["gluecodium_target_python_sources(greeter_cpp)<br/>finds pybind11, globs pybind11/*.cpp"]:::build
        LIBT["add_library(greeter_cpp STATIC ...)<br/>= HABS + HRT + SRCGEN + SRCRT + IMPL"]:::build
        MODT["pybind11_add_module(greeter_python MODULE ...)<br/>= PBINIT + PBREG + PBHDR<br/>links greeter_cpp + pybind11 + Python3"]:::build
    end

    HABS --> LIBT
    HRT --> LIBT
    SRCGEN --> LIBT
    SRCRT --> LIBT
    IMPL --> LIBT

    PBINIT --> MODT
    PBREG --> MODT
    PBHDR --> MODT
    LIBT -->|"link static lib"| MODT
    CMK --> MODT

    %% ---- Built artifacts ----
    LIBA["libgreeter_cpp.a<br/>static C++ library<br/>(abstract classes + impl + runtime)"]:::artifact
    SOSYM["greeter.cpython-314-darwin.so<br/>CPython extension module<br/>(native, importable as 'greeter')"]:::artifact

    LIBT --> LIBA
    MODT --> SOSYM

    %% ---- Runtime bindings ----
    subgraph RT["Installed Python package  (co-located)"]
        direction LR
        RTNAT["greeter.cpython-314-darwin.so"]:::binding
        RTWRP["com/example/greeter/*.py<br/>_native_base.py, __init__.py"]:::binding
    end

    SOSYM --> RTNAT
    PYW --> RTWRP
    PYBASE --> RTWRP

    %% ---- App ----
    subgraph USE["Application  (python/client.py)"]
        direction TB
        IMP["from com.example.greeter.Greeter import Greeter<br/>from com.example.greeter.GreetingListener import GreetingListener"]:::app
        CALL["Greeter.create()<br/>.greet('World') -> str<br/>.add_listener(PrintingListener())<br/>.greeting_count  (property)<br/>.greet('')  -> raises GreeterError"]:::app
    end

    RTNAT --> IMP
    RTWRP --> IMP
    IMP --> CALL

    %% ---- Call path annotation ----
    CALL -.->|"runtime call path"| PATH["Python wrapper .py<br/>-> native .so  (pybind11 register_Greeter)<br/>-> libgreeter_cpp.a  (Greeter::greet)<br/>-> GreeterImpl.cpp  (hand-written body)"]:::app

    classDef source fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#78350f
    classDef tool fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a8a
    classDef gen fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef build fill:#f3e8ff,stroke:#9333ea,stroke-width:2px,color:#581c87
    classDef artifact fill:#ffedd5,stroke:#ea580c,stroke-width:2px,color:#7c2d12
    classDef binding fill:#cffafe,stroke:#0891b2,stroke-width:2px,color:#164e63
    classDef app fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#7f1d1d
```

</details>

---

## 3. Stage-by-Stage Summary

| Stage | Input | Tool / Mechanism | Output |
|-------|-------|------------------|--------|
| **1. Authoring** | — | Developer | `*.lime` (API) + `*Impl.cpp` (C++ bodies) + app `.py` |
| **2. Generation** | `*.lime` | Gluecodium CLI (`-generators cpp,python`) | C++ headers/impl + runtime, Python `.py`/`.pyi` wrappers, pybind11 `.cpp`/`.h` binding sources |
| **3. Compilation** | generated C++ + hand-written impl | CMake (`Gluecodium.cmake`, `Python.cmake`) + C++ compiler | `libgreeter_cpp.a` (C++ lib) + `greeter.cpython-*.so` (extension module) |
| **4. Python bindings** | `.so` + `.py` wrappers | Installed co-located in one dir | Importable Python package (`import greeter`; `from com.example.greeter.Greeter import Greeter`) |
| **5. Apps** | Python bindings | Python interpreter | App calls flow: wrapper `.py` -> native `.so` (pybind11) -> C++ lib -> hand-written impl |

### Key Gluecodium internals (Stage 2)

1. **`lime-loader`** — ANTLR grammar (`LimeIDL.g4`) parses `.lime` text into a parse tree.
2. **`lime-runtime`** — converts the parse tree into the **LIME model** (a language-independent
   `LimeType` tree: structs, classes, interfaces, enums, exceptions, lambdas).
3. **Validators** — check type references, inheritance, overloads, properties, etc.
4. **Generators** (`generator/cpp`, `generator/python`) — each collects names/imports via
   **name resolvers** (`PythonNameRules`, `Pybind11NameResolver`) and applies **Mustache
   templates** (via Trimou) to emit files.
5. **Output** — written under `build/generated/` in `cpp/` and `python/` subtrees.

### Key CMake mechanics (Stage 3)

- **`add_library(greeter_cpp STATIC …)`** — compiles the generated C++ impl skeletons +
  runtime + the developer's `GreeterImpl.cpp` into a static library.
- **`gluecodium_target_python_sources(greeter_cpp …)`** (in `Python.cmake`) — globs
  `python/pybind11/*.cpp`, calls `pybind11_add_module(… MODULE …)`, links the C++ library,
  pybind11, and Python headers, and names the `.so` after the `PYBIND11_MODULE` symbol.
- Because pybind11 validates its source list at **configure** time, generation must run
  first (at configure time via `execute_process`, or at build time followed by a CMake
  re-configure so the glob picks up the generated sources — see the two-pass build in
  `build-python-functional`).

### Runtime call path (Stage 5)

```
Python:  Greeter.create().greet("World")
   |
   v
wrapper:  com/example/greeter/Greeter.py   (thin Python class -> native)
   |
   v
native:   greeter.cpython-314-darwin.so    (pybind11: register_Greeter, trampolines)
   |
   v
C++ lib:  libgreeter_cpp.a                 (Greeter::greet  -- generated abstract decl)
   |
   v
impl:     GreeterImpl.cpp                  (hand-written body -- the actual logic)
```
