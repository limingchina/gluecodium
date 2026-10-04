# Python Calculator example

This example defines an API in LimeIDL, implements it in C++, and calls it from
Python through generated pybind11 bindings. See the
[Python binding guide](../../docs/python_bindings.md) for the API and build reference.

## Requirements

- JDK 17 or newer to build Gluecodium.
- Python 3.10 or newer with development headers.
- CMake 3.19 or newer and a C++17 compiler.
- pybind11 (2.11 or newer).

## Build and run

Run these commands from the **repository root**. Set `JAVA_HOME` to your JDK if
Java is not already available on `PATH`.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'pybind11>=2.11'
./gradlew :gluecodium:installDist

cmake -S examples/python -B build/python-example \
  -DGLUECODIUM_BIN="$PWD/gluecodium/build/install/gluecodium/bin/gluecodium" \
  -DPython3_EXECUTABLE="$(python -c 'import sys; print(sys.executable)')" \
  -Dpybind11_DIR="$(python -m pybind11 --cmakedir)"
cmake --build build/python-example --config Release
ctest --test-dir build/python-example -C Release --output-on-failure
```

For a single-configuration generator (such as Makefiles or Ninja), run:

```bash
(cd build/python-example && python client.py)
```

For a multi-configuration generator, run from the directory containing the built
extension and copied client, for example `build/python-example/Release`.
Use the same Python interpreter for configuration and execution.

The client prints results for addition (`5.0`), subtraction (`5.0`), multiplication
(`42.0`), and division (`4.0`). The listener receives each successful result.
It then reads a calculation count of `4`, resets it to `0`, reports the
`com_example_calculator_CalculatorErrorError` exception for division by zero, and constructs a result
struct in Python. The native exception name includes its LimeIDL package; the
extra `Error` suffix follows the generator's default exception naming rule.

## Files and workflow

| File | Purpose |
| --- | --- |
| [lime/Calculator.lime](lime/Calculator.lime) | Struct, interface, enum, exception, and class definitions. |
| [cpp/CalculatorImpl.cpp](cpp/CalculatorImpl.cpp) | Implements the C++ service and factory. |
| [CMakeLists.txt](CMakeLists.txt) | Generates bindings, builds the extension, and copies Python files. |
| [python/client.py](python/client.py) | Imports generated wrappers and exercises the API. |

CMake invokes Gluecodium at **configure time**, then compiles the generated C++
runtime, the service implementation, and the generated binding sources. The
extension is named `calculator`; wrappers live under `com.example.calculator`.
The generated code is kept under the build directory.

Re-run the CMake configure command after changing LimeIDL or rebuilding Gluecodium.
Use a new build directory when changing Python versions. The wrapper package,
`_native_base.py`, and extension must all be available on Python's import path;
the example copies them beside `client.py` automatically.
