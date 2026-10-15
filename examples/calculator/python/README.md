# Python Calculator example

This project exposes the shared [Calculator LimeIDL API](../lime/Calculator.lime)
and [C++ implementation](../cpp/CalculatorImpl.cpp) through Python bindings.
The same sources are used by the Android and Apple Calculator examples. See the
[Python binding guide](../../../docs/python_bindings.md) for the API and build reference.

## Requirements

- JDK 17 or newer to build Gluecodium.
- Python 3.10 or newer with development headers.
- CMake 3.19 or newer and a C++17 compiler.
- pybind11 3.1.0 or newer.

## Build and run

Run these commands from the **repository root**. Set `JAVA_HOME` to your JDK if
Java is not already available on `PATH`.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'pybind11>=3.1.0'
./gradlew :gluecodium:installDist

cmake -S examples/calculator/python -B build/python-example \
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

The client checks addition (`5`), lambda-based subtraction (`5`), interface-based
multiplication (`42`) and its overflow callback, division via nested structs (`4.0`)
and division-by-zero errors, a returned native interface (`min`), nullable values
(`max`), and an exception raised on sum overflow. Assertions make CTest fail if
these boundary contracts are broken.

## Files and workflow

| File | Purpose |
| --- | --- |
| [../lime/Calculator.lime](../lime/Calculator.lime) | Shared API, nested types, callbacks, and errors. |
| [../cpp/CalculatorImpl.cpp](../cpp/CalculatorImpl.cpp) | Shared C++ implementation and factory. |
| [CMakeLists.txt](CMakeLists.txt) | Generates bindings, builds the extension, and copies Python files. |
| [client.py](client.py) | Imports generated wrappers and exercises the shared API. |

CMake invokes Gluecodium at **configure time**, then compiles the shared C++
implementation, generated runtime and binding sources. `-intnamespace gluecodium`
matches the runtime namespace used by the shared implementation. The native
extension is named `calculator`; public wrappers live under `gluecodium.calculator`.
Generated code is kept under the build directory.

Re-run the CMake configure command after changing LimeIDL or rebuilding Gluecodium.
Use a new build directory when changing Python versions. The wrapper package,
`_native_base.py`, and extension must all be available on Python's import path;
the example copies them beside `client.py` automatically.
