#!/bin/bash
#
# Test harness for the Python detection logic in build-python-functional.
# Extracts the detection functions and runs them under various scenarios.
#
# IMPORTANT: We do NOT use `set -u` here because the real script doesn't either
# (it uses #!/bin/bash -e). Using `set -u` would cause false failures with
# unset GLUECODIUM_PYTHON.

set -eo pipefail

PASS=0
FAIL=0
SCRIPT_DIR="/Volumes/APFS/Work/gluecodium/functional-tests/scripts"

# ── Extract the detection functions from build-python-functional ────────────
. "${SCRIPT_DIR}/inc.functions"

# These are set by the arg parser in the real script; we set them manually.
PYTHON_BIN_OVERRIDE=""
GLUECODIUM_PYTHON="${GLUECODIUM_PYTHON:-}"

_validate_python() {
    local py="$1"
    [[ -x "$py" ]] || return 1
    local version
    version=$("$py" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")' 2>/dev/null) || return 1
    local major minor
    major=${version%%.*}
    minor=${version#*.}
    [[ "$major" -eq 3 && "$minor" -ge 8 ]] || return 1
    "$py" -c 'import pybind11' 2>/dev/null || return 1
    "$py" -m pybind11 --cmakedir >/dev/null 2>&1 || return 1
    return 0
}

detect_python() {
    local candidate
    local candidates=()

    # 1. Explicit override via CLI or env var
    if [[ -n "${PYTHON_BIN_OVERRIDE}" ]]; then
        if _validate_python "${PYTHON_BIN_OVERRIDE}"; then
            echo "${PYTHON_BIN_OVERRIDE}"
            return 0
        fi
        cat >&2 <<ERROR

ERROR: The Python interpreter specified via --python does not meet requirements:
  ${PYTHON_BIN_OVERRIDE}

It must be Python 3.8+ with pybind11 installed (pip install pybind11).
ERROR
        return 1
    elif [[ -n "${GLUECODIUM_PYTHON:-}" ]]; then
        if _validate_python "${GLUECODIUM_PYTHON}"; then
            echo "${GLUECODIUM_PYTHON}"
            return 0
        fi
        cat >&2 <<ERROR

ERROR: The Python interpreter specified via GLUECODIUM_PYTHON does not meet requirements:
  ${GLUECODIUM_PYTHON}

It must be Python 3.8+ with pybind11 installed (pip install pybind11).
ERROR
        return 1
    fi

    # 2. Auto-detection: python3 on PATH
    local path_python
    path_python=$(command -v python3 2>/dev/null || true)
    [[ -n "$path_python" ]] && candidates+=("$path_python")

    # 3. Common conda / miniconda / anaconda paths
    local conda_bases=(
        "$HOME/miniconda3/bin/python3"
        "$HOME/miniconda/bin/python3"
        "$HOME/anaconda3/bin/python3"
        "$HOME/anaconda/bin/python3"
        "/opt/miniconda3/bin/python3"
        "/opt/anaconda3/bin/python3"
        "/usr/local/miniconda3/bin/python3"
        "/usr/local/anaconda3/bin/python3"
    )
    for c in "${conda_bases[@]}"; do
        [[ -x "$c" ]] && candidates+=("$c")
    done

    # 4. Homebrew Python (macOS)
    local brew_bases=(
        "/opt/homebrew/bin/python3"
        "/usr/local/bin/python3"
    )
    for c in "${brew_bases[@]}"; do
        [[ -x "$c" ]] && candidates+=("$c")
    done

    # 5. System Python
    [[ -x "/usr/bin/python3" ]] && candidates+=("/usr/bin/python3")

    # De-duplicate while preserving order
    local seen=""
    local unique=()
    for c in "${candidates[@]}"; do
        local real
        real=$(readlink -f "$c" 2>/dev/null || echo "$c")
        if [[ " $seen " != *" $real "* ]]; then
            seen="$seen $real"
            unique+=("$c")
        fi
    done

    for candidate in "${unique[@]}"; do
        if _validate_python "$candidate"; then
            echo "$candidate"
            return 0
        fi
    done

    cat >&2 <<'ERROR'

ERROR: No suitable Python 3.8+ interpreter with pybind11 was found.
ERROR
    return 1
}

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
# Use /usr/bin/python3 which typically doesn't have pybind11
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
