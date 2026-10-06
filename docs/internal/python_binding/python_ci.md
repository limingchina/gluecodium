# Python bindings CI

The [Python bindings workflow](../../../.github/workflows/python-bindings.yml) runs
on pushes, pull requests, and manual dispatch. It uses Ubuntu 24.04, Python 3.14,
pybind11 **3.1.0**, Java 17, GCC, CMake, and Ninja. The pybind11 version is pinned
in [.github/requirements-python-ci.txt](../../../.github/requirements-python-ci.txt).

The job sets `ORG_GRADLE_PROJECT_kotlinWarningsAsErrors=true`, enabling Kotlin's
warnings-as-errors option for production and test compilation in the `gluecodium`
generator module (including its validators).
Unused parameters, unnecessary casts, and other Kotlin compiler warnings fail the
build. To enable the same check locally, pass `-PkotlinWarningsAsErrors=true` to
Gradle; ordinary local builds keep the default warning behavior.

The workflow runs the parameterized generator `SmokeTest` class, including its
Python cases, to compare generated files with checked-in references. This class
also exercises the other generators; it does not build their platform SDKs.
It then uses the official functional-test script to generate C++/Python bindings,
compile the extension, and run the Python functional suite through CTest:

```bash
python -m pip install -r .github/requirements-python-ci.txt
./gradlew :gluecodium:test --tests com.here.gluecodium.SmokeTest --console=plain
CC=gcc CXX=g++ CMAKE_BUILD_PARALLEL_LEVEL=3 \
  functional-tests/scripts/build-python-functional \
  --buildGluecodium --python "$(command -v python)" --verbose
```

Run these commands from the repository root with Python 3.14 selected and the
native build tools installed. `--python` makes the script use that interpreter
for pybind11 discovery, extension configuration, and tests. The job prints the
interpreter, Python ABI, and pybind11 version before building. For details of the
script's local overrides, see [Python functional tests](python_functional_tests.md).

Gradle and pip dependencies are cached. The compiler cache is separated by
runner/toolchain/Python/pybind11 configuration; its source-hash key restores
previous entries when sources change. Generated files and native build directories
are rebuilt on each run. The job limits native compilation to three concurrent
processes and has a 60-minute timeout.

On failure, download `python-3.14-failure-diagnostics` from the workflow run. It
contains smoke-test reports, build output, CMake configuration, and CTest logs
when those files exist. Compiler-cache statistics are printed even when tests fail.
