# Python bindings

Gluecodium's `python` generator creates Python wrappers and pybind11 binding
sources for a LimeIDL API. Run it together with `cpp`, implement the generated C++
API, and compile the binding sources into a CPython extension. Python code can
then call C++ and implement interfaces that C++ calls back into.

Start with the runnable [Calculator example](../examples/python/README.md).
For LimeIDL syntax, see the [user guide](guide.md) and [language reference](lime_idl.md).

## Requirements

Use Python **3.10 or newer** for the generated wrapper layer. The CMake helper
requires Python 3.10+ to match generated code that uses features such as
`types.UnionType` and built-in generic annotations.
You also need Python development headers, a C++17 compiler, CMake 3.19+ for the
example, and pybind11 3.1.0+ (the minimum declared by generated `pyproject.toml`).
Building Gluecodium from this branch requires a suitable JDK; the example uses
JDK 17 or newer and the repository's Gradle wrapper.

An extension is built for a particular Python ABI and platform. Configure,
build, and run with the same Python version and architecture. Reconfigure in a
fresh build directory after changing interpreters.

## Generate bindings

From the repository root, build the CLI distribution:

```bash
./gradlew :gluecodium:installDist
```

Then generate both layers, for example using the Calculator definition:

```bash
gluecodium/build/install/gluecodium/bin/gluecodium \
  -input examples/python/lime/Calculator.lime \
  -output build/calculator-generated \
  -generators cpp,python \
  -pythonmodule calculator
```

`calculator` is the **native extension module name**. It must match both the compiled
extension filename and its generated `PYBIND11_MODULE` entry point. The LimeIDL
`package com.example.calculator` determines the wrapper package independently.
Choose a simple Python identifier for the native module name and avoid naming it
like a top-level wrapper package, which would cause an import conflict.

### Generated files

For the command above, `build/calculator-generated` contains:

| Path | Purpose |
| --- | --- |
| `cpp/include/`, `cpp/src/` | C++ API declarations, generated implementations, and runtime. |
| `python/com/example/calculator/*.py` | Python wrapper modules, one per top-level element. |
| `python/com/example/calculator/*.pyi` | Matching type stubs. |
| `python/**/__init__.py` | Package initialization files. |
| `python/_native_base.py` | Wrapping, unwrapping, and object identity helpers. |
| `python/pybind11/*.cpp` | Type registrations and `_module_init.cpp` entry point. |
| `python/pybind11/*.h` | Return, locale, collection, and wrapper-cache helpers. |
| `python/setup.py`, `python/pyproject.toml` | Starting points for a setuptools build. |

With separate main and common output directories, inspect both output trees;
shared runtime files may be in the common output. The example uses a single
output directory to keep the build straightforward.

Do not edit generated files to add application logic. Implement the generated C++
classes and factory functions in your own sources, then link those sources and
the generated runtime into the extension.

### Python-specific CLI options

| Option | Default | Meaning |
| --- | --- | --- |
| `-pythonmodule NAME` | `generated` | Native extension module name. |
| `-pythonnamerules FILE` | Built-in rules | Properties file overriding Python naming conventions. |
| `-pythonpackage NAME` | Empty | Parsed package setting; currently not applied by the Python generator. |
| `-pythonintpackage NAME` / `-python-internal-package NAME` | Empty | Parsed internal-package setting; currently not applied by the Python generator. |

Currently, wrapper paths follow the LimeIDL package. Do not rely on the package
options to relocate generated modules. General options such as `-cache`,
`-options`, and `-tags` also apply; use the CLI's `-help` for the full list.

## Build and distribute

### CMake

The [example CMake project](../examples/python/CMakeLists.txt) is a complete
configuration that runs generation before defining the extension target.
The repository's `cmake/modules/gluecodium/Gluecodium.cmake` includes the Python
helper:

```cmake
# my_cpp_api already contains your implementation and generated C++ runtime.
# generated_dir contains cpp/ and python/, generated before this call.
set_target_properties(my_cpp_api PROPERTIES POSITION_INDEPENDENT_CODE ON)
gluecodium_target_python_sources(my_cpp_api
  MODULE_NAME calculator
  OUTPUT_DIR "${generated_dir}"
  OUTPUT python_extension)
```

The helper locates Python 3.10+ and pybind11, gathers `python/pybind11/*.cpp`, creates
`my_cpp_api_python`, and links `my_cpp_api`. `OUTPUT` receives that target's name;
`MODULE_NAME` changes the extension filename, so it must agree with
`-pythonmodule` used during generation.

Without `MODULE_NAME`, the helper uses `GLUECODIUM_PYTHON_MODULE_NAME` on the host
target, then `generated`. Without `OUTPUT_DIR`, it reads the target's
`GLUECODIUM_OUTPUT_MAIN_DIR`, set by Gluecodium's CMake generation machinery.
The corresponding generation properties are `GLUECODIUM_PYTHON_MODULE_NAME`,
`GLUECODIUM_PYTHON_NAMERULES`, `GLUECODIUM_PYTHON_PACKAGE`, and
`GLUECODIUM_PYTHON_INTERNAL_PACKAGE`; the package-setting caveat above also applies.
See the [CMake integration guide](../cmake/README.md) for general target setup.

Ensure binding sources exist **before configuration** of the extension target:
the helper globs existing files and pybind11 requires a source list then. For a
new project, generate at configure time as the example does, or explicitly run
generation before configuring the extension. Re-run configuration after input
changes when using configure-time generation.

Install or copy both the compiled extension and the generated Python files.
The helper builds the extension but does not install the wrapper packages.
Keep their `.pyi` files when packaging if you want consumers to use the stubs.
On Linux, static C++ libraries linked into the extension need position-independent
code; use `POSITION_INDEPENDENT_CODE ON`.

### Setuptools

The emitted `setup.py` lists only `pybind11/*.cpp`. Before using it for a wheel,
add your C++ implementation and generated runtime sources (or link the library
that contains them), include paths for the generated C++ headers, C++17 settings,
and package discovery/data for the wrapper modules and stubs. The emitted build
files alone do not package a complete application API.

## Use the generated API

Import wrapper types from their individual modules:

```python
from com.example.calculator.Calculator import Calculator
from com.example.calculator.Calculation import Calculation
from com.example.calculator.CalculationListener import CalculationListener

calculator = Calculator.create()
print(calculator.add(2.0, 3.0).value)
calculator.calculation_count = 10
result = Calculation("2 + 3", 5.0)
```

Both the wrapper root (the directory containing `com/` and `_native_base.py`)
and the extension's directory must be on `sys.path`, for example by installing
them together or setting `PYTHONPATH`. Adding only the generated `com/` directory
is insufficient. Importing the wrappers loads the native extension automatically.

### Names and attributes

Types use `UpperCamelCase`; methods, parameters, fields, and properties use
`lower_snake_case`; enum members and constants use `UPPER_SNAKE_CASE`.
Thus `setListener` becomes `set_listener` and `calculationCount` becomes
`calculation_count`. Hard Python keywords gain a trailing underscore.
Nested types remain nested under their containing wrapper type, for example
`Outer.Inner`; their native registration identifiers are an implementation detail.

Use Python attributes in LimeIDL to customize output:

```lime
@Python(Name = "RenamedService")
class Service {
    @Python(Name = "run")
    fun execute()

    @Python(Skip)
    fun platformOnly()

    @Python(Internal)
    fun implementationDetail()
}
```

`Name` overrides the generated name. `Skip` hides an element from Python bindings.
`Internal` conventionally prefixes names with `_`; it does not enforce access
control. An explicit `Name` takes priority over the internal prefix.
See [naming conventions](naming_conventions.md) for naming-rule properties.

### Equatable structs and collection keys

Equatable structs compare by value. Mutable structs are unhashable, including
immutable outer structs that contain mutable state. A deeply immutable struct
with immutable scalar or struct fields retains value hashing.

Use `value.as_key()` to create an immutable snapshot for a dictionary or set.
The snapshot compares by value with the original struct and owns a native copy;
nested getters and instance methods operate on detached copies. Native map and
set results automatically expose struct keys as snapshots. For example:

```python
key = Maps.EquatableStruct("id").as_key()
values = Maps.struct_to_string_round_trip({key: "saved"})
```

Snapshots reject graphs containing shared value-equatable class or interface
references, or shared blobs, because copying the struct cannot isolate their
mutable value state. Private native struct objects use identity equality and
hashing for transport; public wrappers provide the documented value semantics.

### Type mappings

| LimeIDL | Python representation |
| --- | --- |
| `Void` | `None` |
| `Boolean` | `bool` |
| Integer types | `int` (C++ range still applies) |
| `Float`, `Double` | `float` |
| `String` | `str` |
| `Blob` | `bytes` |
| `Date` | `datetime.datetime` |
| `Duration` | `datetime.timedelta` |
| `Locale` | BCP 47 language-tag `str`, such as `"en-US"` |
| `T?` | `Optional[T]`, accepting `None` |
| `List<T>`, `Set<T>`, `Map<K,V>` | `list`, `set`, `dict` |
| `lambda` | `typing.Callable` |
| `enum` | Generated `enum.Enum` wrapper |
| `struct` | Generated value wrapper with fields and constructors |
| `class`, `interface` | Generated wrappers around shared C++ objects |

Collection contents are converted recursively. Collections used as dictionary
keys or set elements use hashable representations: lists become tuples, sets
become frozensets, and maps become frozensets of key/value tuples.
Structs cross the boundary as values; changing a returned struct does not mutate
a previously passed C++ value. Classes and interfaces use shared ownership.
The wrapper cache reuses class/interface wrappers by native identity and selects
the most specific bound wrapper for regular inherited views. Polymorphic base
subobjects share the same identity. Narrow-interface requests keep their declared
view and a separate cache entry. Cache entries are weak: identity is preserved
while a public wrapper is alive, and dropping its last application reference
allows its native shared ownership to be released. If C++ still owns the native
object, a later return creates a new public wrapper. Native address reuse cannot
recover an expired wrapper.

The cache does not own callback objects. Keep Python interface owners alive until
native callbacks finish. A native `std::function` retains its Python callable until
native code releases the function; join or drain workers before interpreter
shutdown.

### Callbacks

Subclass the generated interface, initialize its base, and override its Python
method names:

```python
class PrintingListener(CalculationListener):
    def __init__(self):
        super().__init__()

    def on_calculated(self, result: Calculation) -> None:
        print(result.expression, result.value)

listener = PrintingListener()
calculator.set_listener(listener)
calculator.multiply(6.0, 7.0)
```

Callback arguments and return values use the same public wrapper types as ordinary
method calls, including wrappers inside nullable values and collections. Override
interface methods or Python properties with public types; callable parameters and
results also convert their arguments and returns when invoked through C++.
Direct Python calls to your overrides retain ordinary Python behavior.

Generated native methods, factories, property accessors, and returned native
callables release the GIL while executing C++ work. Python argument and result
conversions run with the GIL held, and trampolines acquire it before invoking
Python overrides. Plain generated struct field access remains serialized by the
GIL. Native implementations must synchronize their own state when calls run
concurrently.

Join or explicitly drain native workers before releasing callback owners or
shutting down Python. Native worker code must catch callback exceptions and
propagate them after joining; exceptions must not escape a `noexcept` callback.
Keep the Python callback object alive while C++ may invoke it;
shared ownership of a C++ object alone is not a substitute for managing the Python
subclass's lifetime.

### Errors

A successful C++ `Return<T, Error>` becomes a Python value (`None` for `Void`).
A failure raises a registered Python exception, falling back to `RuntimeError`
when no mapping exists. For enum-backed errors, the native extension exposes the
exception type with a package-qualified registration name (as in the example
below); for struct-backed errors, the translator resolves the generated
Python exception class. Error messages come from the C++ error description.

```python
import calculator as native

try:
    calculator.divide(1.0, 0.0)
except native.com_example_calculator_CalculatorErrorError as error:
    print(error)
```

The default exception naming rule adds an `Error` suffix, so the LimeIDL name
`CalculatorError` becomes `CalculatorErrorError`; the native registration also
includes the package prefix. Do not assume every generated wrapper exception class
is the same exception type raised by the native layer. Enum-backed errors share a `std::error_code` registry
entry, so APIs with multiple enum-backed exception definitions need particular
care: the current registry maps by C++ error type, not individual enum type.
Payload exceptions currently carry a message, rather than all fields of the
original C++ payload.

## Current limits and troubleshooting

- Python `@Async`/`asyncio` integration is not provided. Use synchronous APIs or
  explicit callbacks; the Python functional suite does not enable the Async feature.
- Package override options are parsed but do not change wrapper output paths.
- Generated setuptools files need application-specific build and packaging setup.

For `ModuleNotFoundError`, check both the native module name and wrapper import
root. An import error mentioning an undefined C++ symbol usually indicates missing
implementation or runtime sources in the linked library. A missing module with a
`cpython-...` suffix can indicate an interpreter/ABI mismatch; rebuild with the
interpreter you use to run the client.

If a callback reports a pure virtual call, check the subclass's base initializer,
override names, and lifetime. If generated code appears stale, re-run generation
and CMake configuration before rebuilding.

For contributor verification, use the [Python functional-test guide](internal/python_functional_tests.md).
Feature coverage is defined in `functional-tests/functional/CMakeLists.txt` and
`functional-tests/functional/python/test/`; historical development plans are not
an up-to-date support matrix.
