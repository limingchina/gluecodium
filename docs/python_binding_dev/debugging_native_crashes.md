# Debugging Native Crashes in pybind11 Extensions

> **Audience**: AI agents (tmux workflow) and human developers (manual workflow)
> **Context**: Gluecodium Python generator functional tests

The pybind11 extension module (`functional.cpython-<SOABI>.so`) is a native shared
library loaded by CPython. Crashes (segfaults, EXC_BAD_ACCESS, aborts) in the
generated C++ binding code or in pybind11 internals require a native debugger.

This document covers two debugging workflows:

1. **[AI Agent Workflow (tmux + LLDB)](#ai-agent-workflow-tmux--lldb)** — for AI
   agents that need to drive LLDB non-interactively via shell commands.
2. **[Manual Debugging Workflow](#manual-debugging-workflow)** — for human
   developers who can attach to an interactive terminal.

---

## Prerequisites (both workflows)

| Tool | Requirement | How to verify |
|------|-------------|---------------|
| **LLDB** | Installed (system default on macOS via Xcode CLT) | `lldb --version` |
| **Python** | Same interpreter that built the `.so` (see below) | `which python3` |
| **Build** | Functional tests built at least once | `ls functional-tests/build-python/functional/functional.cpython-*.so` |

For the tmux workflow only: `tmux` must be installed (`brew install tmux` if missing; verify with `tmux -V`).

## Key paths

```
# Python interpreter (auto-detected by python-env.sh)
PYTHON_BIN="$(cd functional-tests && . scripts/python-env.sh; echo $PYTHON_BIN)"
# e.g. /Users/<user>/miniconda3/bin/python3

# Extension module (.so)
SO_PATH="functional-tests/build-python/functional/functional.cpython-312-darwin.so"

# Test directory (where pytest runs)
TEST_DIR="functional-tests/build-python/functional/python"

# PYTHONPATH (so `import functional` and `import test` resolve correctly)
PYTHONPATH="functional-tests/build-python/functional"
```

## Python interpreter must match the build

The pybind11 extension module's SOABI suffix is derived from the Python headers
used at CMake configure time. A `.so` built against Python 3.12 **cannot** be
loaded by Python 3.9, and vice versa. Always use the same interpreter that
`build-python-functional` detected (it prints the path during the build):

```
>>> Detecting Python interpreter (with pybind11)
  Using: /Users/l2ming/miniconda3/bin/python3 (Python 3.12.3)
```

To override, pass `--python /path/to/python3` to `build-python-functional` or
set `GLUECODIUM_PYTHON` before building. See
`functional-tests/scripts/python-env.sh` for the full detection logic.

---

## AI Agent Workflow (tmux + LLDB)

> **Use this workflow when**: You are an AI agent or need to drive LLDB
> non-interactively through shell commands. The tmux session keeps debugger
> state alive across tool calls.

### Step 1: Create (or reuse) a tmux session

```bash
# Check for an existing session
tmux ls 2>/dev/null

# Create a new one if needed
tmux new-session -d -s debug
```

### Step 2: Launch LLDB targeting the Python interpreter

Because LLDB's `settings set target.run-args` does not handle `-m` correctly
(it treats `-m` as an LLDB option), create a small wrapper script instead:

```bash
cat > functional-tests/build-python/functional/python/run_tests.py << 'EOF'
import sys
import pytest
sys.exit(pytest.main(["tests/", "-v"]))
EOF
```

Then launch LLDB inside the tmux session:

```bash
tmux send-keys -t debug \
  "cd /Volumes/APFS/Work/gluecodium/functional-tests/build-python/functional/python && \
   PYTHONPATH=/Volumes/APFS/Work/gluecodium/functional-tests/build-python/functional \
   lldb $(which python3) run_tests.py" \
  Enter
```

### Step 3: Run and capture the crash

```bash
# Start the program
tmux send-keys -t debug 'run' Enter

# Wait for it to stop (segfault / breakpoint / etc.), then capture output
sleep 5
tmux capture-pane -pt debug -S -100
```

### Step 4: Inspect the crash

```bash
# Get the backtrace
tmux send-keys -t debug 'thread backtrace' Enter
sleep 1
tmux capture-pane -pt debug -S -100

# Inspect frame variables
tmux send-keys -t debug 'frame variable' Enter
sleep 1
tmux capture-pane -pt debug -S -20

# Set breakpoints and re-run
tmux send-keys -t debug 'breakpoint set --name register_test_Lambdas' Enter
tmux send-keys -t debug 'run' Enter
sleep 2
tmux capture-pane -pt debug -S -50
```

### Step 5: Teardown

```bash
# Quit LLDB
tmux send-keys -t debug 'quit' Enter

# Kill the tmux session
tmux kill-session -t debug
```

### Operating rules for AI agents

This workflow follows the `lldb-tmux-debugging` skill
(`~/.agents/skills/lldb-tmux-debugging/SKILL.md`). Key rules:

- **Prefer tmux** over direct interactive attachment so debugger state
  persists across turns.
- **Use `tmux send-keys` / `tmux capture-pane`** for all debugger
  interaction — never assume the debugger accepted a command until the
  pane output confirms it.
- **Do not kill an existing `debug` session** unless a clean restart is
  required; reuse it to preserve breakpoints and state.
- **Capture enough evidence** at each stop: stop reason, current frame,
  backtrace, and key locals/registers.
- **Clean up the session** when debugging is complete:
  `tmux kill-session -t debug`.

---

## Manual Debugging Workflow

> **Use this workflow when**: You are a human developer with access to an
> interactive terminal. This is the fastest way to debug when you can
> directly type commands into LLDB.

### Step 1: Open a terminal and navigate to the test directory

```bash
cd /Volumes/APFS/Work/gluecodium/functional-tests/build-python/functional/python
```

### Step 2: Set up environment variables

```bash
export PYTHONPATH="/Volumes/APFS/Work/gluecodium/functional-tests/build-python/functional"
```

### Step 3: Create a test runner script (one-time setup)

```bash
cat > run_tests.py << 'EOF'
import sys
import pytest
sys.exit(pytest.main(["tests/", "-v"]))
EOF
```

### Step 4: Launch LLDB with the Python interpreter

```bash
lldb $(which python3) run_tests.py
```

You should see the LLDB prompt `(lldb)`.

### Step 5: Set breakpoints (optional but recommended)

```lldb
# Break on a specific registration function
(lldb) breakpoint set --name register_test_Lambdas

# Or break on a source file location
(lldb) breakpoint set --file _module_init.cpp --line 42

# Or break on a C++ exception throw
(lldb) breakpoint set --name __cxa_throw
```

### Step 6: Run the program

```lldb
(lldb) run
```

The program will execute and stop at breakpoints or crash points.

### Step 7: Inspect the crash or breakpoint

When the program stops, gather evidence:

```lldb
# Show the stop reason and current frame
(lldb) thread backtrace          # or just 'bt'

# Show all local variables in the current frame
(lldb) frame variable

# Show specific variables
(lldb) frame variable this
(lldb) frame variable *this

# Show CPU registers (useful for EXC_BAD_ACCESS)
(lldb) register read

# Evaluate an expression in the current frame
(lldb) expression this->member_
```

### Step 8: Navigate the call stack

```lldb
# List all frames
(lldb) thread backtrace

# Select a specific frame
(lldb) frame select 3

# Show locals in that frame
(lldb) frame variable
```

### Step 9: Continue or step through code

```lldb
# Resume execution
(lldb) continue

# Step over (next line, not into function calls)
(lldb) next

# Step into function calls
(lldb) step

# Step out of current function
(lldb) finish
```

### Step 10: Re-run after making changes

If you modified C++ code and rebuilt:

```lldb
# Quit LLDB
(lldb) quit

# Rebuild
cd /Volumes/APFS/Work/gluecodium/functional-tests
./scripts/build-python-functional --publish

# Relaunch LLDB and repeat from Step 4
```

### Quick reference: common LLDB commands

| Command | Short | Purpose |
|---------|-------|---------|
| `thread backtrace` | `bt` | Show the full call stack at the crash point |
| `frame select <n>` | `f 3` | Switch to frame `n` in the backtrace |
| `frame variable` | `v` | Show local variables in the current frame |
| `image lookup -s <sym>` | | Find a symbol in the binary |
| `breakpoint set --name <fn>` | `b <fn>` | Set a breakpoint by function name |
| `breakpoint set --file <f> --line <n>` | `b <f>:<n>` | Set a breakpoint by source location |
| `expression <expr>` | `p <expr>` | Evaluate a C++ expression |
| `register read` | `re r` | Show CPU registers |
| `continue` | `c` | Resume execution |
| `next` | `n` | Step over |
| `step` | `s` | Step into |
| `finish` | | Step out of current function |
| `quit` | `q` | Exit LLDB |

### Tips for manual debugging

1. **Use tab completion**: LLDB supports tab completion for commands,
   function names, and file names. Type `b reg` then Tab to see matching
   breakpoint names.

2. **Use the TUI mode**: Press `Ctrl+X` to toggle LLDB's text UI mode,
   which shows source code alongside the debugger prompt.

3. **Add commands to `.lldbinit`**: Create `~/.lldbinit` with default
   settings, e.g.:
   ```
   settings set target.x86-disassembly-flavor intel
   command script import ~/.lldb/custom_formatters.py
   ```

4. **Debug vs Release builds**: For the most detailed backtraces, build
   with `CMAKE_BUILD_TYPE=Debug`:
   ```bash
   cd functional-tests && ./scripts/build-python-functional --publish -- -DCMAKE_BUILD_TYPE=Debug
   ```

---

## Common pybind11 Debugging Scenarios

### Segfault on exit (EXC_BAD_ACCESS in `pthread_mutex_lock`)

This is almost always a GIL teardown ordering issue. During `Py_Exit` →
`__cxa_finalize_ranges`, C++ static destructors (e.g. `~std::function`)
try to acquire the GIL via `pybind11::gil_scoped_acquire`, but the GIL
has already been destroyed. Look for `gil_scoped_acquire` in the
backtrace frames.

### `PyInit_functional` not found

The extension module failed to compile or is stale. Check `ninja` output
for compilation errors, then force a clean rebuild:

```bash
rm -rf functional-tests/build-python/functional/gluecodium
rm -f functional-tests/build-python/functional/functional.cpython-*.so
cd functional-tests && ./scripts/build-python-functional --publish
```

### SOABI mismatch (`ImportError: dynamic module does not define module export function`)

The `.so` was built with a different Python version than the one running
the tests. Ensure `PYTHONPATH` and the Python binary both match the
build-time interpreter.

### Reproducing exit-time crashes

`run-python-tests` may **not** trigger exit-time segfaults because `pytest`
calls `os._Exit()` which bypasses `atexit` handlers and static destructor
ordering. Use CTest instead:

```bash
cd functional-tests/build-python && ctest -R python --verbose
```

Or run the Python process directly (not through pytest) to trigger normal
shutdown:

```bash
PYTHONPATH=... python3 -c "import functional; ..."
```

### Debugging import-time crashes

If the crash happens during `import functional` (module initialization),
set a breakpoint on the module init function:

```lldb
(lldb) breakpoint set --name PyInit_functional
(lldb) run
```

Or break on pybind11's internal module creation:

```lldb
(lldb) breakpoint set --name pybind11::detail::make_new_python_type
```

### Debugging callback / trampoline issues

For crashes in virtual function overrides (trampoline classes):

```lldb
# Break on the trampoline method
(lldb) breakpoint set --name "MyTrampoline::onCallback"

# Or break on all pure virtual calls (abstract method not implemented)
(lldb) breakpoint set --name __cxa_pure_virtual
```

---

## Reference

- **LLDB tutorial**: https://lldb.llvm.org/use/tutorial.html
- **pybind11 FAQ**: https://pybind11.readthedocs.io/en/stable/faq.html
- **lldb-tmux-debugging skill**: `~/.agents/skills/lldb-tmux-debugging/SKILL.md`
