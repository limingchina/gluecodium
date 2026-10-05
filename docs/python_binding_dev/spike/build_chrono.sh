#!/bin/bash
# Build the Date/Duration chrono spike and run its test.
set -euo pipefail

cd "$(dirname "$0")"

CXX="${CXX:-c++}"
PYTHON="${PYTHON:-python3}"

INCLUDES="$("$PYTHON" -m pybind11 --includes)"
if [ -z "$INCLUDES" ]; then
    INCLUDES="-I$("$PYTHON" -c 'import pybind11; print(pybind11.get_include())')"
    INCLUDES="$INCLUDES -I$("$PYTHON" -c 'import sysconfig; print(sysconfig.get_path("include"))')"
fi

# Static vs shared Python link strategy (see spike_return_caster.md).
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
OUT="chrono_spike${SUFFIX}"

echo ">> Compiling $OUT"
$CXX -O2 -std=c++17 -fPIC -shared $INCLUDES chrono_spike.cpp -o "$OUT" $LINKFLAGS

echo ">> Running test_chrono.py"
"$PYTHON" test_chrono.py
