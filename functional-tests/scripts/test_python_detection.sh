#!/bin/bash
#
# Copyright (C) 2016-2025 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

# Test harness for the Python detection logic in python-env.sh.
# Runs detect_python() under various scenarios to verify correctness.
#
# Usage:  ./scripts/test_python_detection.sh

set -eo pipefail

PASS=0
FAIL=0
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Source the shared detection logic
. "${SCRIPT_DIR}/inc.functions"
. "${SCRIPT_DIR}/python-env.sh"

# ── Test helpers ────────────────────────────────────────────────────────────

assert_ok() {
    local name="$1"
    local result
    if result=$(detect_python 2>/dev/null); then
        echo "  PASS: $name -> $result"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name -> detection failed"
        FAIL=$((FAIL + 1))
    fi
}

assert_fail() {
    local name="$1"
    local result
    if result=$(detect_python 2>/dev/null); then
        echo "  FAIL: $name -> should have failed but got: $result"
        FAIL=$((FAIL + 1))
    else
        echo "  PASS: $name -> correctly failed"
        PASS=$((PASS + 1))
    fi
}

assert_equals() {
    local name="$1"
    local expected="$2"
    local result
    result=$(detect_python 2>/dev/null) || true
    local real_expected real_result
    real_expected=$(readlink -f "$expected" 2>/dev/null || echo "$expected")
    real_result=$(readlink -f "$result" 2>/dev/null || echo "$result")
    if [[ "$real_result" == "$real_expected" ]]; then
        echo "  PASS: $name -> $result"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name -> expected $expected, got $result"
        FAIL=$((FAIL + 1))
    fi
}

# ── Determine what's available on this machine ─────────────────────────────

CONDA_PYTHON="$HOME/miniconda3/bin/python3"
SYSTEM_PYTHON="/usr/bin/python3"
PATH_PYTHON=$(command -v python3 2>/dev/null || echo "")

echo "=== Environment Probe ==="
echo "  PATH python3:       ${PATH_PYTHON:-<not found>}"
echo "  Conda python3:      $CONDA_PYTHON ($([[ -x "$CONDA_PYTHON" ]] && echo 'exists' || echo 'missing'))"
echo "  System python3:     $SYSTEM_PYTHON ($([[ -x "$SYSTEM_PYTHON" ]] && echo 'exists' || echo 'missing'))"
if [[ -n "$PATH_PYTHON" ]]; then
    echo "  PATH python version: $($PATH_PYTHON --version 2>&1)"
    echo "  PATH python pybind11: $($PATH_PYTHON -c 'import pybind11; print(pybind11.__version__)' 2>/dev/null || echo '<not installed>')"
fi
if [[ -x "$CONDA_PYTHON" ]]; then
    echo "  Conda python version: $($CONDA_PYTHON --version 2>&1)"
    echo "  Conda python pybind11: $($CONDA_PYTHON -c 'import pybind11; print(pybind11.__version__)' 2>/dev/null || echo '<not installed>')"
fi
if [[ -x "$SYSTEM_PYTHON" ]]; then
    echo "  System python version: $($SYSTEM_PYTHON --version 2>&1)"
    echo "  System python pybind11: $($SYSTEM_PYTHON -c 'import pybind11; print(pybind11.__version__)' 2>/dev/null || echo '<not installed>')"
fi
echo ""

# ── Tests ───────────────────────────────────────────────────────────────────

echo "=== Test 1: Auto-detection (no override) ==="
PYTHON_BIN_OVERRIDE=""
unset GLUECODIUM_PYTHON 2>/dev/null || true
assert_ok "auto-detect finds a valid Python"

echo ""
echo "=== Test 2: --python override with valid interpreter (conda) ==="
if [[ -x "$CONDA_PYTHON" ]] && _validate_python "$CONDA_PYTHON"; then
    PYTHON_BIN_OVERRIDE="$CONDA_PYTHON"
    assert_equals "override -> conda python" "$CONDA_PYTHON"
else
    echo "  SKIP: conda python not available or lacks pybind11"
fi

echo ""
echo "=== Test 3: --python override with non-existent path ==="
PYTHON_BIN_OVERRIDE="/nonexistent/python3"
assert_fail "override -> non-existent path"

echo ""
echo "=== Test 4: --python override with Python missing pybind11 ==="
if [[ -x "$SYSTEM_PYTHON" ]] && ! _validate_python "$SYSTEM_PYTHON"; then
    PYTHON_BIN_OVERRIDE="$SYSTEM_PYTHON"
    assert_fail "override -> python without pybind11"
else
    echo "  SKIP: system python has pybind11 or doesn't exist"
fi

echo ""
echo "=== Test 5: GLUECODIUM_PYTHON env var override ==="
if [[ -x "$CONDA_PYTHON" ]] && _validate_python "$CONDA_PYTHON"; then
    PYTHON_BIN_OVERRIDE=""
    export GLUECODIUM_PYTHON="$CONDA_PYTHON"
    assert_equals "env var -> conda python" "$CONDA_PYTHON"
    unset GLUECODIUM_PYTHON
else
    echo "  SKIP: conda python not available or lacks pybind11"
fi

echo ""
echo "=== Test 6: GLUECODIUM_PYTHON env var with invalid path ==="
PYTHON_BIN_OVERRIDE=""
export GLUECODIUM_PYTHON="/nonexistent/python3"
assert_fail "env var -> non-existent path"
unset GLUECODIUM_PYTHON

echo ""
echo "=== Test 7: --python takes precedence over GLUECODIUM_PYTHON ==="
if [[ -x "$CONDA_PYTHON" ]] && _validate_python "$CONDA_PYTHON"; then
    PYTHON_BIN_OVERRIDE="$CONDA_PYTHON"
    export GLUECODIUM_PYTHON="/nonexistent/python3"
    assert_equals "CLI override takes precedence over env var" "$CONDA_PYTHON"
    unset GLUECODIUM_PYTHON
else
    echo "  SKIP: conda python not available"
fi

echo ""
echo "=== Test 8: Auto-detection finds conda when PATH python lacks pybind11 ==="
PYTHON_BIN_OVERRIDE=""
unset GLUECODIUM_PYTHON 2>/dev/null || true
if [[ -x "$CONDA_PYTHON" ]] && _validate_python "$CONDA_PYTHON"; then
    SAVED_PATH="$PATH"
    export PATH="/usr/bin:/bin"
    if ! command -v python3 >/dev/null 2>&1 || ! _validate_python "$(command -v python3)"; then
        assert_equals "conda found when PATH python lacks pybind11" "$CONDA_PYTHON"
    else
        echo "  SKIP: PATH python also has pybind11, can't distinguish"
    fi
    export PATH="$SAVED_PATH"
else
    echo "  SKIP: conda python not available or lacks pybind11"
fi

echo ""
echo "=== Test 9: All candidates fail (no python at all) ==="
PYTHON_BIN_OVERRIDE=""
unset GLUECODIUM_PYTHON 2>/dev/null || true
SAVED_PATH="$PATH"
SAVED_HOME="$HOME"
export PATH="/dev/null"
export HOME="/nonexistent"
assert_fail "no python available anywhere"
export PATH="$SAVED_PATH"
export HOME="$SAVED_HOME"

echo ""
echo "==============================================="
echo "Results: $PASS passed, $FAIL failed"
echo "==============================================="
exit $FAIL
