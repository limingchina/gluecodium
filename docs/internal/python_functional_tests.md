Python functional tests
=======================

This document covers running the Python (pybind11) functional tests for Gluecodium.
For the general functional-test workflow, see
[Testing](../../AGENTS.md#testing) and [testing.md](testing.md).

Basic command
-------------

```bash
functional-tests/scripts/build-python-functional --publish
```

This builds Gluecodium, publishes it to the local Maven repository, generates the
C++ and Python binding sources, compiles the pybind11 extension module, and runs
the pytest suite via CTest — all with a single command.

Python version must match between build and test (pybind11 / `.so` SOABI)
-------------------------------------------------------------------------

The Python (pybind11) functional build compiles a CPython extension module
(`functional.cpython-<SOABI>.so`) whose SOABI suffix is derived from the Python
headers/libs that `find_package(Python ...)` resolves at CMake configure time
(see `cmake/modules/gluecodium/Python.cmake`). The compiled `.so` can **only** be
imported by the *same* Python version that built it — a 3.9 interpreter cannot load a
`cpython-314` module, and vice versa.

To keep the build and test interpreter in sync, `build-python-functional`
auto-detects a Python 3.8+ interpreter with pybind11 installed (see
`functional-tests/scripts/python-env.sh`). It probes the following locations in
order: `python3` on `PATH`, common conda/miniconda/anaconda paths, Homebrew
Python, and system Python. The detected interpreter's bin directory is prepended
to `PATH` and passed to CMake via `-DPython_EXECUTABLE=...`, so both the build
and the pytest runner use the same interpreter. **No manual `PATH` prefixing is
required**.

Overriding the interpreter
--------------------------

To force a specific interpreter (e.g. a particular conda env or Homebrew Python),
pass `--python /path/to/python3` or set the `GLUECODIUM_PYTHON` env var:

```bash
# Via CLI flag
functional-tests/scripts/build-python-functional --publish --python /path/to/python3

# Via env var
GLUECODIUM_PYTHON=/path/to/python3 functional-tests/scripts/build-python-functional --publish
```

When an explicit interpreter is given, the script validates that it is Python 3.8+
with pybind11 installed and does **not** fall back to auto-detection — so an invalid
override fails loudly instead of silently picking another interpreter.

Requirements for any interpreter (auto-detected or overridden):

- Python 3.8 or newer
- `pybind11` installed (`pip install pybind11`)

If you change the used python version, do a clean rebuild:

```bash
rm -rf functional-tests/build-python
```

so the cache re-detects Python and the `.so` is recompiled with the matching SOABI.

Stale generated code after editing generator templates/sources
--------------------------------------------------------------

The functional-test build scripts run `publishToMavenLocal` first, then drive
CMake, which shells out to Gradle to run Gluecodium and emit the generated
`.cpp`/`.py` files. **The CMake custom command that invokes Gradle depends only
on the LimeIDL inputs and the generated options/config file — it does NOT depend
on the published Gluecodium jar.**

Consequence: if you change a generator template
(`gluecodium/src/main/resources/templates/**`) or generator Kotlin source,
re-run `publishToMavenLocal`, and then rebuild **without any change to the
`.lime` inputs**, CMake considers code generation "up-to-date" and skips the
Gradle step. The previously generated (now stale) `.cpp`/`.py` files are left in
place and compiled, so your template fix appears to have no effect (or you get
confusing errors from old output).

How to force regeneration after a generator change:

- Touch/modify a relevant `.lime` input (e.g. re-save it), OR
- Delete the generated output directory before rebuilding, e.g.
  `rm -rf functional-tests/build-python/functional/gluecodium`, OR
- Use `--buildGluecodium` (which sets `GLUECODIUM_PATH` to the local source tree)
  so the build uses the working copy directly instead of the published jar — but
  note the same up-to-date check still applies to the LimeIDL inputs, so a clean
  of the generated dir is still required when only templates changed.

Always verify the regenerated file actually reflects your change (check its
timestamp and content) before concluding a fix failed.

Build script options
--------------------

`build-python-functional` accepts the following options:

- `--publish` — Build and publish Gluecodium locally and use it for code generation.
- `--buildGluecodium` — Build and use the local Gluecodium source tree directly.
- `--gluecodiumPath [PATH]` — Implies `--buildGluecodium`; path to local Gluecodium.
- `--python [PATH]` — Path to a Python interpreter with pybind11 installed (default: auto-detect).
- `--debug` — Build with debug symbols.
- `--verbose` — Print Gluecodium/Gradle code-generation output (recommended for debugging hangs).
- `--quiet` — Suppress the verbose Gluecodium/Gradle code-generation output.
- `--help` — Print the help message.

Environment variables:

- `GLUECODIUM_PYTHON` — Same as `--python`; takes precedence over auto-detection.
- `GLUECODIUM_VERBOSE` — Set to `ON` to enable verbose code-generation output.
