#!/bin/bash
# Build the Return<T, Error> spike as a CPython extension module and run the test.
set -euo pipefail

cd "$(dirname "$0")"

CXX="${CXX:-c++}"
PYTHON="${PYTHON:-python3}"

# pybind11 + Python include flags
INCLUDES="$("$PYTHON" -m pybind11 --includes)"
# Fallback if the module isn't importable that way
if [ -z "$INCLUDES" ]; then
    INCLUDES="-I$("$PYTHON" -c 'import pybind11; print(pybind11.get_include())')"
    INCLUDES="$INCLUDES -I$("$PYTHON" -c 'import sysconfig,sys; print(sysconfig.get_path("include"))')"
fi

# Link flags for the Python runtime.
# The conda Python here is a STATIC build (Py_ENABLE_SHARED=0, libpython3.12.a).
# Linking libpython into the extension creates a second interpreter copy and
# crashes with "GIL is released". The correct approach for static Python is to
# leave the Python symbols undefined and let the host interpreter resolve them
# at load time via -undefined dynamic_lookup.
PY_ENABLE_SHARED="$("$PYTHON" -c 'import sysconfig; print(sysconfig.get_config_var("Py_ENABLE_SHARED"))')"
if [ "$PY_ENABLE_SHARED" = "1" ]; then
    LINKFLAGS="$("$PYTHON" -c 'import sysconfig
libdir=sysconfig.get_config_var("LIBDIR") or ""
base="python" + sysconfig.get_config_var("VERSION")
print(f"-L{libdir} -l{base}")')"
else
    LINKFLAGS="-undefined dynamic_lookup"
fi

SUFFIX="$("$PYTHON" -c 'import sysconfig; print(sysconfig.get_config_var("EXT_SUFFIX"))')"
OUT="spike_module${SUFFIX}"

echo ">> Compiling $OUT"
$CXX -O2 -std=c++17 -fPIC -shared $INCLUDES spike_module.cpp -o "$OUT" $LINKFLAGS

echo ">> Running test_spike.py"
"$PYTHON" test_spike.py
