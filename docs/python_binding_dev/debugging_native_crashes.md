# Debugging Python native failures

Use the interpreter that configured and built the extension. Python headers,
pybind11 discovery, test execution and the extension's SOABI must agree. Start
with the [functional-test guide](../internal/python_functional_tests.md) and use
`--debug` for debug symbols. Regenerate after template changes before trusting a
rebuild; a timestamp-only CMake rule can otherwise leave stale bindings in place.

## Reproduce under a native debugger

From the repository root, substitute the interpreter used for the build:

```bash
export PYTHONPATH="$PWD/functional-tests/build-python/functional:$PWD/functional-tests/build-python/functional/python"
lldb -- /path/to/python -m pytest functional-tests/build-python/functional/python/tests/ -x -v
# Alternatively:
gdb --args /path/to/python -m pytest functional-tests/build-python/functional/python/tests/ -x -v
```

At the LLDB prompt, use `run`, `thread backtrace all`, `frame select N`, and
`frame variable`. GDB equivalents are `run`, `thread apply all bt`, `frame N`,
and `info locals`. A debugger is required on the host; permission to attach and
symbol availability depend on its configuration. Prefer a focused test after
reproducing the failure with the full test command.

For a hang, interrupt the process and collect all thread stacks. A Python caller
waiting in native `join` while its worker waits for the GIL suggests a release-scope
problem. Inspect the actual generated C++: argument/result conversion and Python
holder management require the GIL, while real blocking native work releases it.
A Python traceback alone cannot show which native mutex or worker is waiting.

For an exit-time crash, check whether workers were drained before Python teardown,
Python interface owners remained alive, and retained native callables were released.
Weak wrapper caching is not a worker-shutdown or interface-owner policy. Avoid
calling Python or destroying retained Python state after interpreter finalization.

For an import/link failure, check the extension name against `-pythonmodule`, the
ABI suffix, wrapper import root, and linked implementation/runtime sources. Do not
manually link a second interpreter into an extension as a substitute for the
platform's pybind11/CMake module configuration.

Preserve the generated source, interpreter/pybind11 versions, CMake cache, complete
thread stacks and smallest failing public call with a bug report. CI uploads
[diagnostics](../internal/python_ci.md) on failure. Do not assume a particular
signal implies one cause without examining those stacks.
