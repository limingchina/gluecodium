# Gluecodium Python Generator Plan (pybind11 Approach)

> **Status**: Design phase
> **Author**: l2ming
> **Date**: 2026-07-13
> **Related**: Based on the existing Gluecodium architecture (using the Dart FFI / Swift CBridge generators as reference)

---

## 1. Background and Motivation

Gluecodium currently supports five target languages: C++ / Java / Kotlin / Swift / Dart. Python, as a mainstream language in data science, machine learning, and automated testing, is increasingly in demand in cross-platform projects.

### 1.1 Approach Selection: pybind11

| Approach | Advantages | Disadvantages |
|----------|------------|---------------|
| **ctypes/cffi over C-ABI shim** | Reuses Dart FFI's C-ABI layer, zero compile-time dependency | Requires manual implementation of reference counting, exception marshalling, and GIL-safe callbacks |
| **pybind11 generated bindings** ✅ | Automatically handles reference counting, exception conversion, GIL, and STL container conversion; less generated code | Adds a compile-time dependency (pybind11 + compiled extension module); deviates architecturally from the JNI/FFI pattern |

**Reasons for choosing pybind11**:
- Python's GIL and object model fit naturally with pybind11
- Reference counting, exception marshalling, and callback thread-safety are handled by the pybind11 framework, greatly reducing the complexity of the generated code
- CPython itself is a compiled extension module, so the compile dependency is acceptable for the Python ecosystem
- pybind11 is the most mature C++ binding framework in the CPython ecosystem, with an active community

### 1.2 Architecture Comparison

```
Existing Dart architecture:
  LimeIDL → LIME Model → DartGenerator
    ├── Dart code (dart/ffi calls)
    └── FFI C++ code (C-ABI shim → C++ API)

Existing Swift architecture:
  LimeIDL → LIME Model → SwiftGenerator
    ├── Swift code
    └── CBridge C/C++ code (C-ABI shim → C++ API)

New Python architecture (pybind11):
  LimeIDL → LIME Model → PythonGenerator
    ├── Python code (.py + .pyi type stubs)
    └── pybind11 C++ code (wraps the C++ API directly, no C-ABI intermediate layer)
```

**Key difference**: The pybind11 approach does not need a C-ABI intermediate layer (unlike Dart FFI / Swift CBridge); pybind11's `.cpp` binding files directly `#include` the C++ headers and call the C++ API.

---

## 2. Implementation Phases

### Phase 0 — Prerequisites

#### 0.1 Confirm pybind11 version and dependencies
- pybind11 >= 2.11.0 (supports C++17, Python 3.8+)
- Target platforms: Linux (gcc/clang), macOS (clang), Windows (MSVC)
- Python: 3.8+ (aligned with pybind11's minimum supported version)

#### 0.2 Verify C++ generator compatibility
- Confirm that the headers produced by the existing C++ generator can be directly `#include`d by pybind11
- Confirm conversion support in pybind11 for types such as `std::optional`, `std::vector`, `std::map`, `std::set`
- Confirm the feasibility of exception mapping for the `Return<T, Error>` type in pybind11

---

### Phase 1 — LIME Model Layer Extensions

#### 1.1 Add the `PYTHON` attribute type

**File**: `lime-runtime/src/main/java/com/here/gluecodium/model/lime/LimeAttributeType.kt`

```kotlin
// Add to the enum:
PYTHON("Python", LimeAttributeValueType.NAME),
```

This enables LimeIDL to use the `@Python` attribute:
```lime
@Python(Name = "customName")
class MyClass { ... }

@Python(Skip)
class InternalOnly { ... }

@Python(Internal)
fun internalMethod() { ... }
```

#### 1.2 Update the annotation converter

**File**: `lime-loader/src/main/java/com/here/gluecodium/loader/AntlrLimeConverter.kt`

Add to the `convertAnnotationType()` method:
```kotlin
"Python" -> LimeAttributeType.PYTHON
```

In the `propagateParentAttributes()` method, add `PYTHON` to the traversal list:
```kotlin
listOf(JAVA, SWIFT, DART, KOTLIN, PYTHON).forEach { ... }
```

#### 1.3 Add Python naming rules

**New file**: `gluecodium/src/main/resources/namerules/python.properties`

```properties
field=snake_case
parameter=snake_case
constant=UPPER_SNAKE_CASE
enumerator=UPPER_SNAKE_CASE
method=snake_case
property=snake_case
property.prefix.boolean=is
type=UpperCamelCase
error=UpperCamelCase
error.suffix=Error
join.infix=_
```

#### 1.4 Update `GeneratorOptions`

**File**: `gluecodium/src/main/java/com/here/gluecodium/generator/common/GeneratorOptions.kt`

Add Python-related option fields:
```kotlin
var pythonPackages: List<String> = listOf(),
var pythonInternalPackages: List<String> = listOf(),
var pythonNameRules: Configuration = ConfigurationProperties.fromResource(
    Gluecodium::class.java, "/namerules/python.properties"
),
var pythonModule: String = "generated",  // Python module name
```

> **Status**: ✅ Implemented in Phase 1 (commit `be4747f9a`). The CLI options from
> Phase 2.4 were also pulled forward and implemented as part of Phase 1 (see §2.4 and
> `docs/python_binding_dev/phase1_implementation.md` §1.5), since the options/CLI layer
> is needed for end-to-end use and is harmless to add before the generator exists.

---

### Phase 2 — Generator Skeleton

#### 2.1 Create the Python generator package

```
gluecodium/src/main/java/com/here/gluecodium/generator/python/
├── PythonGenerator.kt              # Main generator class, implements the Generator interface
├── PythonNameResolver.kt           # LIME → Python name resolution
├── Pybind11NameResolver.kt         # LIME → C++ pybind11 name resolution
├── PythonImportResolver.kt         # Python import resolution
├── PythonImportsCollector.kt       # Python import collector
├── Pybind11IncludeResolver.kt      # C++ include resolution
├── PythonGeneratorPredicates.kt    # Template predicates
├── PythonCommentsProcessor.kt      # Documentation comment processing
├── PythonOverloadsValidator.kt     # Overloads validator
├── Pybind11Helpers.kt              # pybind11 helper utilities
└── package-info.java
```

#### 2.2 Implement the `PythonGenerator` class

**File**: `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGenerator.kt`

Modeled after the structure of `DartGenerator`:

```kotlin
internal class PythonGenerator : Generator {
    override val shortName = "python"

    override fun initialize(options: GeneratorOptions) {
        // Initialize naming rules, namespace, module name, etc.
    }

    override fun generate(limeModel: LimeModel): List<GeneratedFile> {
        // 1. Filter the model (LimeModelSkipPredicates + PYTHON attribute)
        // 2. Create the name resolvers
        // 3. Run validators
        // 4. For each top-level element, generate:
        //    a. Python module file (.py)
        //    b. pybind11 binding file (.cpp)
        // 5. Generate common files (setup.py, __init__.py, type conversion, etc.)
    }
}
```

The generator produces two categories of files:
- **MAIN**: Each top-level LIME element corresponds to one `.py` file and one `.cpp` pybind11 binding file
- **COMMON**: `setup.py`/`pyproject.toml`, type conversion helper code, `__init__.py`

#### 2.3 Register the generator

**File**: `gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator`

Add a line:
```
com.here.gluecodium.generator.python.PythonGenerator
```

#### 2.4 CLI option support

> **Status**: ✅ Implemented in Phase 1 (commit `be4747f9a`). Pulled forward from Phase 2
> because the options/CLI layer is required for end-to-end use and is safe to add before
> the generator exists. See `docs/python_binding_dev/phase1_implementation.md` §1.5 for the
> verification (all four options appear in `-help`, `@Python` parses via `-validate`).

**File**: `gluecodium/src/main/java/com/here/gluecodium/cli/OptionReader.kt`

Add CLI options:
```kotlin
addOption("pythonpackage", true, "Python package name for generated sources")
addOption("pythonintpackage", "python-internal-package", true, 
    "Python sub-package for internal types")
addOption("pythonmodule", true, "Name of the generated Python extension module")
addOption("pythonnamerules", true, "Python name rules property file")
```

Add the corresponding option parsing logic in the `read()` method.

---

### Phase 3 — Template System

> **Status**: ✅ Implemented (commit `TBD` — see `docs/python_binding_dev/phase3_implementation.md`).
> Core per-type templates (class/interface/struct/enum/exception) plus shared partials
> (function/property/field) generate real Python wrappers and pybind11 `register_*`
> functions. Module init (`PYBIND11_MODULE`) and common files (setup.py/pyproject) are
> Phase 6.

#### 3.1 Create Mustache templates

**Directory**: `gluecodium/src/main/resources/templates/python/`

```
templates/python/
├── PythonFile.mustache              # Python file skeleton
├── PythonClass.mustache             # Python class definition
├── PythonInterface.mustache         # Python interface/protocol
├── PythonStruct.mustache            # Python struct (dataclass)
├── PythonEnumeration.mustache       # Python enumeration
├── PythonException.mustache         # Python exception class
├── PythonLambda.mustache            # Python callback type
├── PythonProperty.mustache          # Python property
├── PythonFunction.mustache          # Python function declaration
├── PythonFunctionBody.mustache      # Python function body (calls native)
├── PythonField.mustache             # Python field
├── PythonDocumentation.mustache     # docstring
├── PythonImport.mustache            # import statement
├── PythonAttributes.mustache        # attribute decorators
├── PythonSetupPy.mustache           # setup.py build script
├── PythonPyproject.mustache         # pyproject.toml
├── PythonInit.mustache              # __init__.py
├── Pybind11Module.mustache          # pybind11 module entry point
├── Pybind11Class.mustache           # pybind11 class binding
├── Pybind11Struct.mustache          # pybind11 struct binding
├── Pybind11Enum.mustache            # pybind11 enum binding
├── Pybind11Function.mustache        # pybind11 function binding
├── Pybind11Property.mustache        # pybind11 property binding
├── Pybind11Exception.mustache       # pybind11 exception mapping
├── Pybind11Lambda.mustache          # pybind11 callback wrapper
└── Pybind11TypeCaster.mustache      # custom type caster
```

#### 3.2 pybind11 binding template example

**`Pybind11Class.mustache`** (conceptual example):
```cpp
// 为 class {{resolveName}} 生成 pybind11 绑定
py::class_<{{resolveName "C++"}}, {{trampolineClassName}}>(module, "{{resolveName}}")
    .def(py::init<>(){{#constructors}}, py::init<{{constructorArgs}}>(){{/constructors}})
    {{#functions}}
    .def("{{resolveName}}", &{{resolveName "C++"}}::{{resolveName "C++"}}, 
         py::arg("{{paramName}}"){{#defaultValue}} = {{.}}{{/defaultValue}})
    {{/functions}}
    {{#properties}}
    .def_property("{{resolveName}}", 
                  &{{resolveName "C++"}}::{{getterName}},
                  &{{resolveName "C++"}}::{{setterName}})
    {{/properties}}
    ;
```

**`Pybind11Module.mustache`** (conceptual example):
```cpp
#include <pybind11/pybind11.h>
#include "{{headerInclude}}"

PYBIND11_MODULE({{moduleName}}, m) {
    m.doc() = "{{documentation}}";

    {{#elements}}
    {{> Pybind11Class}}
    {{/elements}}
}
```

#### 3.3 Python code template example

**`PythonClass.mustache`** (conceptual example):
```python
class {{resolveName}}({{parentClass}}):
    """{{documentation}}"""

    {{#properties}}
    @property
    def {{resolveName}}(self) -> {{resolveType typeRef}}:
        return self._native.{{resolveName}}

    {{/properties}}

    {{#functions}}
    def {{resolveName}}(self{{#parameters}}, {{name}}: {{type}}{{/parameters}}) -> {{returnType}}:
        """{{documentation}}"""
        return self._native.{{resolveName}}({{#parameters}}{{name}}{{/parameters}})

    {{/functions}}
```

---

### Phase 4 — Type Mapping

> **Status**: ✅ Implemented (commit `TBD` — see `docs/python_binding_dev/phase4_implementation.md`).
> Basic types (incl. Date/Duration/Locale), compound types (List/Set/Map/nullable), and
> typealias/lambda all map correctly. The `Return<T,Error>` pybind11 caster is generated as a
> common header (`_return_caster.h`), proven from the Phase 0 spike.

#### 4.1 Basic type mapping

| LIME type | C++ type | Python type | pybind11 conversion |
|-----------|----------|-------------|--------------------|
| `Void` | `void` | `None` | `void` |
| `Boolean` | `bool` | `bool` | automatic |
| `Byte` | `int8_t` | `int` | automatic |
| `Short` | `int16_t` | `int` | automatic |
| `Int` | `int32_t` | `int` | automatic |
| `Long` | `int64_t` | `int` | automatic |
| `UByte` | `uint8_t` | `int` | automatic |
| `UShort` | `uint16_t` | `int` | automatic |
| `UInt` | `uint32_t` | `int` | automatic |
| `ULong` | `uint64_t` | `int` | automatic |
| `Float` | `float` | `float` | automatic |
| `Double` | `double` | `float` | automatic |
| `String` | `std::string` | `str` | automatic |
| `Blob` | `std::vector<uint8_t>` | `bytes` | automatic |
| `Date` | `std::chrono::system_clock::time_point` | `datetime.datetime` | custom caster |
| `Duration` | `std::chrono::nanoseconds` | `datetime.timedelta` | custom caster |
| `Locale` | custom Locale type | `str` (BCP 47) or custom | custom caster |

#### 4.2 Compound type mapping

| LIME type | C++ type | Python type | pybind11 handling |
|-----------|----------|-------------|------------------|
| `List<T>` | `std::vector<T>` | `list[T]` | automatic (requires `#include <pybind11/stl.h>`) |
| `Set<T>` | `std::unordered_set<T>` | `set[T]` | automatic |
| `Map<K,V>` | `std::unordered_map<K,V>` | `dict[K,V]` | automatic |
| `T?` (nullable) | `std::optional<T>` | `Optional[T]` | automatic (requires `#include <pybind11/stl.h>`) |

#### 4.3 User-defined type mapping

| LIME type | C++ type | Python type | pybind11 handling |
|-----------|----------|-------------|------------------|
| `struct` | C++ struct/class | `@dataclass` or plain class | pybind11 `py::class_` binding |
| `class` | C++ abstract class | Python class (wraps C++ pointer) | pybind11 `py::class_` + trampoline |
| `interface` | C++ pure virtual class | Python ABC/Protocol | pybind11 trampoline + `py::class_` |
| `enum` | C++ enum | `enum.Enum` | pybind11 `py::enum_` |
| `exception` | C++ exception | Python Exception subclass | pybind11 `py::exception` + exception translation |
| `lambda` | C++ `std::function` | Python callable | pybind11 automatic conversion |
| `typealias` | C++ `using`/`typedef` | Python type alias | declared in `.pyi` |

#### 4.4 Date/Duration custom type caster

**`Pybind11TypeCaster.mustache`** (conceptual example):
```cpp
#include <pybind11/chrono.h>
#include <chrono>

namespace pybind11::detail {
    // Date: time_point ↔ datetime.datetime
    template<>
    struct type_caster<std::chrono::system_clock::time_point> {
        PYBIND11_TYPE_CASTER(std::chrono::system_clock::time_point, _("datetime.datetime"));
        
        static handle cast(const std::chrono::system_clock::time_point &src, return_value_policy, handle parent) {
            // Convert time_point to datetime.datetime
            ...
        }
        
        static bool load(handle src, bool) {
            // Convert datetime.datetime to time_point
            ...
        }
    };
}
```

---

### Phase 5 — Object Lifecycle and Callbacks

#### 5.1 Object lifecycle management

pybind11 manages reference counting automatically, but the following needs attention:

**C++ → Python (return values)**:
- pybind11 uses `return_value_policy::automatic` by default
- For functions returning pointers to C++ objects, an appropriate policy must be configured:
  - `return_value_policy::reference_internal` — object lifetime is bound to the Python wrapper
  - `return_value_policy::take_ownership` — Python takes ownership

**Python → C++ (argument passing)**:
- pybind11 handles value and reference passing automatically
- For interface implementations (Python class inheriting a C++ interface), a trampoline class is needed

#### 5.2 Referential Equality

Gluecodium requires referential equality to be preserved across language boundaries. The pybind11 approach needs:

1. **Wrapper Cache**: Maintain a mapping table from `C++ pointer → Python object`
2. When C++ returns a pointer to an existing object, look it up in the cache and return the same Python object
3. Model after Dart's `InstanceCache` and Swift's `WrapperCache` implementations

**`Pybind11WrapperCache.mustache`** (conceptual example):
```cpp
// Wrapper cache: C++ raw pointer → Python object
class WrapperCache {
public:
    static WrapperCache& instance() { ... }
    
    py::object get_or_create(void* cpp_ptr, py::object (*creator)()) {
        auto it = cache.find(cpp_ptr);
        if (it != cache.end()) {
            return it->second;
        }
        auto obj = creator();
        cache[cpp_ptr] = obj;
        return obj;
    }
    
private:
    std::unordered_map<void*, py::object> cache;
};
```

#### 5.3 C++ → Python callbacks (GIL safety)

When a C++ thread calls a Python callback, the GIL must be held:

```cpp
// In the trampoline class:
void onCallback(int value) override {
    py::gil_scoped_acquire gil;  // Acquire the GIL
    PYBIND11_OVERRIDE(void, BaseClass, onCallback, value);
}
```

**Key points**:
- All trampoline methods' `PYBIND11_OVERRIDE` macros need `py::gil_scoped_acquire` inside
- If a callback may be triggered from a non-Python thread, ensure the Python interpreter is initialized
- Model after Dart's `CallbacksQueue` and `IsolateContext` mechanisms

#### 5.4 Exception mapping

| C++ exception | Python exception |
|---------------|----------------|
| `std::exception` | `RuntimeError` |
| Gluecodium `Return<T, Error>` failure | generated `Error` subclass exception |
| `std::bad_optional_access` | `ValueError` |
| `std::out_of_range` | `IndexError` |
| `std::invalid_argument` | `ValueError` |

**`Pybind11Exception.mustache`** (概念示例):
```cpp
// 注册自定义异常
static py::exception<MyError> exc(m, "MyError");
py::register_exception_translator([](std::exception_ptr p) {
    try { if (p) std::rethrow_exception(p); }
    catch (const MyError &e) {
        PyErr_SetString(exc.ptr(), e.what());
    }
});
```

#### 5.5 Async support (`@Async`)

- `@Async` functions map to Python `asyncio` coroutines
- pybind11 bindings return a `Future` object, awaited on the Python side
- `PyGILState_Ensure`/`Release` is needed to acquire the GIL and set the result when the background thread completes
- Model after Dart's `DartAsyncHelpers` for the async bridge

---

### Phase 6 — Output File Structure

#### 6.1 Generated file layout

```
output/
├── python/                              # Python source code
│   ├── __init__.py                      # Package initialization (COMMON)
│   ├── setup.py                         # Build script (COMMON)
│   ├── pyproject.toml                   # PEP 518 build configuration (COMMON)
│   ├── _type_converters.py              # Internal type conversion helpers (COMMON)
│   ├── _wrapper_cache.py                # Reference cache (COMMON)
│   ├── _native_base.py                  # Native base wrapper (COMMON)
│   └── src/                             # Generated Python sources
│       └── <package_path>/
│           ├── __init__.py
│           ├── <module>.py              # Python interface for each top-level LIME element
│           └── <module>.pyi             # Type stubs
│
└── pybind11/                            # pybind11 C++ binding sources
    ├── <module>_bindings.cpp            # pybind11 binding for each top-level element
    ├── _wrapper_cache.h                 # Wrapper cache (COMMON)
    ├── _type_casters.h                  # Custom type casters (COMMON)
    └── _module_init.cpp                 # Module initialization (COMMON)
```

#### 6.2 Build artifacts

The build produces a Python extension module:
- Linux: `.<module_name>.cpython-3x-x86_64-linux-gnu.so`
- macOS: `.<module_name>.cpython-3x-darwin.so`
- Windows: `.<module_name>.cp3x-win_amd64.pyd`

---

### Phase 7 — CMake Integration

#### 7.1 Add the Python generator to the CMake supported list

**File**: `cmake/modules/gluecodium/gluecodium/KnownOptionalProperties.cmake`

Add Python-related CMake target properties:
```cmake
_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_PACKAGE
  BRIEF_DOCS "The base Python package to use for generated Python sources"
  FULL_DOCS "The base Python package to use for generated Python sources."
)

_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_INTERNAL_PACKAGE
  BRIEF_DOCS "The sub-package to use for internal Python code"
  FULL_DOCS "The sub-package to use for internal Python code."
)

_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_MODULE_NAME
  BRIEF_DOCS "Name of the generated Python extension module"
  FULL_DOCS "Name of the generated Python extension module for pybind11."
)

_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_NAMERULES
  BRIEF_DOCS "The path to a file with name rules for Python"
  FULL_DOCS "The path to a file with name rules for Python."
)
```

#### 7.2 Update the generated files list

**File**: `cmake/modules/gluecodium/gluecodium/details/ListGeneratedFiles.cmake`

Add Python/pybind11 file collection logic:
```cmake
if(python IN_LIST _generators)
  list(APPEND _python_generated_files
              "${_unity_dir}/${GLUECODIUM_GENERATED_python_${_group}}")
  list(APPEND _pybind11_generated_files
              "${_unity_dir}/${GLUECODIUM_GENERATED_pybind11_${_group}}")
endif()
```

#### 7.3 Add Python to the supported generators list

**File**: `cmake/modules/gluecodium/gluecodium/details/ReadRequiredProperties.cmake`

Ensure `python` is in the `GLUECODIUM_SUPPORTED_GENERATORS` list.

**File**: `cmake/tests/utils/get_supported_gluecodium_generators.cmake`

```cmake
find_program(_python_exe python3)
if(_python_exe)
  list(APPEND _gluecodium_generator python)
endif()
```

#### 7.4 pybind11 CMake integration

**New file**: `cmake/modules/gluecodium/Python.cmake`

```cmake
# Python module: find pybind11 and configure the Python extension module build
function(gluecodium_target_python_sources _target)
  find_package(pybind11 REQUIRED)
  
  # Get the generated pybind11 .cpp files
  get_target_property(_pybind11_sources ${_target} GLUECODIUM_PYBIND11_SOURCES)
  
  # Create the Python extension module
  pybind11_add_module(${_target}_python ${_pybind11_sources})
  target_link_libraries(${_target}_python PRIVATE ${_target})
endfunction()
```

---

### Phase 8 — Testing

#### 8.1 Smoke tests (unit tests)

**Directory**: `gluecodium/src/test/resources/smoke/`

Add `output/python/` and `output/pybind11/` output directories for each existing smoke test case.

Modeled after the existing Dart smoke test structure:
```
smoke/basic_types/
├── input/
│   └── BasicTypes.lime
└── output/
    ├── cpp/
    ├── dart/
    └── python/              # new
        └── src/
            └── smoke/
                └── basic_types.py
    └── pybind11/            # new
        └── basic_types_bindings.cpp
```

Update the smoke test Java classes to add assertions for the Python generator.

#### 8.2 Functional tests

**New directory**: `functional-tests/functional/python/`

```
functional-tests/functional/python/
├── CMakeLists.txt
├── conftest.py                      # pytest 配置
├── pyproject.toml.in                # 模板 pyproject.toml
└── test/
    ├── basic_types_test.py
    ├── classes_test.py
    ├── enums_test.py
    ├── structs_test.py
    ├── interfaces_test.py
    ├── exceptions_test.py
    ├── lambdas_test.py
    ├── inheritance_test.py
    ├── nullable_test.py
    ├── collections_test.py
    ├── dates_test.py
    ├── durations_test.py
    ├── equatable_test.py
    ├── constants_test.py
    ├── defaults_test.py
    ├── method_overloads_test.py
    ├── nesting_test.py
    ├── properties_test.py
    ├── ref_equality_test.py
    ├── listeners_test.py
    ├── async_test.py
    ├── external_types_test.py
    └── skip_element_test.py
```

**`CMakeLists.txt`** (modeled after `functional-tests/functional/dart/CMakeLists.txt`):
```cmake
cmake_minimum_required(VERSION 3.10)
project(test_python)

if(NOT FUNCTIONAL_BUILD_PYTHON_TESTS)
  return()
endif()

find_program(PYTHON_EXE python3)
find_package(pybind11 REQUIRED)

# Build the Python extension module
pybind11_add_module(functional_python ${PYBIND11_SOURCES})
target_link_libraries(functional_python PRIVATE functional)

# Run pytest
add_test(NAME unit_tests_python
  COMMAND ${PYTHON_EXE} -m pytest test/
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
```

#### 8.3 Functional test build script

**New file**: `functional-tests/scripts/build-python-functional`

Modeled after `build-dart-functional`:
```bash
#!/bin/bash
# Build the Python functional tests
# 1. Run Gluecodium to generate C++ + Python code
# 2. Use CMake to compile the C++ library and pybind11 extension module
# 3. Run pytest
```

---

### Phase 9 — Documentation

#### 9.1 Update the user guide

**File**: `docs/guide.md`
- Add Python generator usage instructions
- Add a `-generators cpp,python` usage example

#### 9.2 Update the LimeIDL reference

**File**: `docs/lime_idl.md`
- Add the `@Python` attribute description

#### 9.3 Update the attributes reference

**File**: `docs/lime_attributes.md`
- Add `@Python(Name=...)`, `@Python(Skip)`, `@Python(Internal)`, `@Python(Public)` descriptions

#### 9.4 Update the external types documentation

**File**: `docs/external_types.md`
- Add the Python external type descriptor block format

#### 9.5 Add Python-specific documentation

**New file**: `docs/python.md`
- Python generator architecture description
- pybind11 dependencies and build requirements
- Type mapping table
- Async support description
- GIL and thread-safety notes

---

### Phase 10 — Gradle Plugin Support

**File**: `gluecodium-gradle/src/main/java/com/here/gluecodium/gradle/GluecodiumExtension.kt` (or the corresponding file)

Add Python-related Gradle configuration:
```groovy
gluecodium {
    pythonPackage = 'com.example.myapp'
    pythonModuleName = 'myapp_native'
}
```

---

## 3. Implementation Order

```
Phase 1 (LIME model layer)
    │
    ├──→ Phase 2 (Generator skeleton) ──→ Phase 3 (Template system)
    │                                    │
    │                                    └──→ Phase 4 (Type mapping)
    │                                              │
    │                                              └──→ Phase 5 (Lifecycle and callbacks)
    │                                                        │
    │                                                        └──→ Phase 6 (Output structure)
    │                                                                  │
    │                                                                  └──→ Phase 7 (CMake)
    │                                                                            │
    └──────────────────────────────────────────────────────────→ Phase 8 (Testing)
                                                                                       │
                                                                                       └──→ Phase 9-10 (Docs and plugin)
```

**Suggested incremental delivery milestones**:

| Milestone | Content | Estimated effort |
|-----------|---------|------------------|
| **M1** | Phase 1-2: LIME attribute + generator skeleton + CLI registration + basic framework working | 3-5 days |
| **M2** | Phase 3-4: Templates + basic type/struct/enum mapping | 5-7 days |
| **M3** | Phase 5: class/interface + callbacks + GIL + referential equality | 7-10 days |
| **M4** | Phase 4 cont.: collections/exceptions/nullable + Phase 6: output structure refinement | 3-5 days |
| **M5** | Phase 7: CMake integration | 2-3 days |
| **M6** | Phase 8: Smoke tests + functional tests | 5-7 days |
| **M7** | Phase 9-10: Docs + Gradle plugin | 2-3 days |

**Total estimate**: 4-6 weeks

---

## 4. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| pybind11 support for the `Return<T, Error>` type requires a custom converter | Medium | Verify the feasibility of a `Return<T, Error>` type_caster early |
| GIL deadlock risk (C++ holds a lock while calling back into Python) | High | Strictly use `py::gil_scoped_acquire`/`py::gil_scoped_release` in trampolines |
| Referential equality implementation complexity | Medium | Model after Dart's mature `InstanceCache` and Swift's `WrapperCache` implementations |
| Multi-platform compilation (Windows MSVC + pybind11) | Medium | Add Windows build tests in CI |
| Python GIL vs C++ thread interaction | High | Clarify the threading model in the design doc, model after Dart's isolate mechanism |
| pybind11 version compatibility | Low | Pin the minimum version to 2.11.0, CI matrix testing |

---

## 5. List of Files to Modify

### New files
| File path | Description |
|-----------|-------------|
| `gluecodium/src/main/java/.../generator/python/*.kt` | Python generator implementation (~10 files) |
| `gluecodium/src/main/resources/templates/python/*.mustache` | Mustache templates (~25 files) |
| `gluecodium/src/main/resources/namerules/python.properties` | Python naming rules |
| `functional-tests/functional/python/*` | Python functional tests |
| `functional-tests/scripts/build-python-functional` | Python test build script |
| `cmake/modules/gluecodium/Python.cmake` | CMake Python module |
| `docs/python.md` | Python generator documentation |

### Modified files
| File path | Change |
|-----------|--------|
| `lime-runtime/.../LimeAttributeType.kt` | Add the `PYTHON` enum value |
| `lime-loader/.../AntlrLimeConverter.kt` | Add `"Python"` annotation parsing |
| `gluecodium/.../common/GeneratorOptions.kt` | Add Python option fields |
| `gluecodium/.../cli/OptionReader.kt` | Add Python CLI options |
| `gluecodium/src/main/resources/META-INF/services/...Generator` | Register PythonGenerator |
| `cmake/.../KnownOptionalProperties.cmake` | Add Python CMake properties |
| `cmake/.../ListGeneratedFiles.cmake` | Add Python file collection |
| `cmake/.../get_supported_gluecodium_generators.cmake` | Add Python detection |
| `docs/guide.md` | Add Python usage instructions |
| `docs/lime_idl.md` | Add `@Python` attribute description |
| `docs/lime_attributes.md` | Add `@Python` attribute reference |
| `docs/external_types.md` | Add Python external type description |
| `AGENTS.md` | Update the supported languages list and structure description |

---

## 6. Acceptance Criteria

- [ ] `./gradlew build` passes (including the new smoke tests)
- [ ] `-generators cpp,python` successfully generates Python + pybind11 C++ code
- [ ] The generated pybind11 code compiles on Linux/macOS/Windows
- [ ] Functional tests cover all existing test cases (aligned with Dart/Swift)
- [ ] Referential equality tests pass
- [ ] GIL-safe callback tests pass
- [ ] `@Python(Skip)` / `@Python(Internal)` / `@Python(Name=...)` attributes work correctly
- [ ] Documentation is complete, including usage guide and type mapping table
