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

# Shared Python interpreter detection for Gluecodium functional test scripts.
#
# The pybind11 extension module's SOABI suffix is tied to the Python version that
# built it, so the *same* interpreter must be used for both building and testing.
# This script auto-detects a Python 3.8+ interpreter with pybind11 installed.
#
# Usage:
#   SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
#   . "${SCRIPT_DIR}/python-env.sh"
#
#   # Option A: Let the caller set PYTHON_BIN_OVERRIDE before calling
#   PYTHON_BIN_OVERRIDE="/path/to/python3"
#   resolve_python
#
#   # Option B: Just call resolve_python — it reads PYTHON_BIN_OVERRIDE
#   # and GLUECODIUM_PYTHON env var, falling back to auto-detection.
#   resolve_python
#
# After resolve_python returns successfully:
#   PYTHON_BIN           — absolute path to the detected Python interpreter
#   PYTHON_VERSION       — version string (e.g. "Python 3.12.3")
#   PYBIND11_CMAKE_DIR   — pybind11 CMake module directory
#   PATH                 — prepended with the interpreter's bin directory
#
# Override precedence (highest to lowest):
#   1. PYTHON_BIN_OVERRIDE  (set by the caller, typically from --python CLI flag)
#   2. GLUECODIUM_PYTHON    (environment variable)
#   3. Auto-detection       (python3 on PATH, conda, Homebrew, system Python)

# Check that a Python interpreter is version >= 3.8 and has pybind11.
_validate_python() {
    local py="$1"

    # Must exist and be executable
    [[ -x "$py" ]] || return 1

    # Must be Python 3.8+
    local version
    version=$("$py" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")' 2>/dev/null) || return 1
    local major minor
    major=${version%%.*}
    minor=${version#*.}
    [[ "$major" -eq 3 && "$minor" -ge 8 ]] || return 1

    # Must be able to import pybind11 and report its CMake directory
    "$py" -c 'import pybind11' 2>/dev/null || return 1
    "$py" -m pybind11 --cmakedir >/dev/null 2>&1 || return 1

    return 0
}

# Detect a suitable Python interpreter.
# Echoes the path on stdout, returns 0 on success, 1 on failure.
detect_python() {
    local candidate
    local candidates=()

    # 1. Explicit override via CLI or env var
    #    When an override is given, ONLY try that interpreter — do not fall
    #    back to auto-detection. The user asked for a specific one.
    if [[ -n "${PYTHON_BIN_OVERRIDE:-}" ]]; then
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
        "/opt/homebrew/bin/python3"   # Apple Silicon
        "/usr/local/bin/python3"       # Intel Mac / Linuxbrew
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

    # Nothing found — print a helpful error
    cat >&2 <<'ERROR'

ERROR: No suitable Python 3.8+ interpreter with pybind11 was found.

The Python functional tests require a Python interpreter that has pybind11
installed (used to build the CPython extension module). The following
locations were checked:

  - python3 on PATH
  - ~/miniconda3, ~/miniconda, ~/anaconda3, ~/anaconda
  - /opt/miniconda3, /opt/anaconda3
  - /opt/homebrew/bin/python3, /usr/local/bin/python3
  - /usr/bin/python3

To fix this:
  1. Install pybind11:  pip install pybind11
  2. Or specify an interpreter explicitly:
       --python /path/to/python3
       # or:
       GLUECODIUM_PYTHON=/path/to/python3 <script>

ERROR
    return 1
}

# Resolve the Python interpreter and set up the environment.
# Sets: PYTHON_BIN, PYTHON_VERSION, PYBIND11_CMAKE_DIR
# Exports: PATH (prepended with the interpreter's bin directory)
# Exits the script on failure (calls die from inc.functions).
resolve_python() {
    PYTHON_BIN=$(detect_python) || die "Python detection failed"
    PYTHON_VERSION=$("$PYTHON_BIN" --version 2>&1)
    PYBIND11_CMAKE_DIR=$("$PYTHON_BIN" -m pybind11 --cmakedir)

    echo "  Using: $PYTHON_BIN ($PYTHON_VERSION)"
    echo "  pybind11 CMake dir: $PYBIND11_CMAKE_DIR"

    # Export so that CMake's find_package(Python) and any subprocesses see the same
    # interpreter on PATH (CMake's Python_EXECUTABLE is set explicitly by callers,
    # but some tools may still fall back to PATH).
    export PATH="$(dirname "$PYTHON_BIN"):$PATH"
}
