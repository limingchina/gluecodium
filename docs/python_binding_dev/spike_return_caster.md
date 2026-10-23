# Spike — `Return<T, Error>` pybind11 type_caster

> **Status**: ✅ Proven (compiles + runs on macOS/arm64, Python 3.12.3, pybind11 3.0.4)
> **Date**: 2026-07-12
> **Related**: `phase0_precheck.md` (the only remaining Phase 0 blocker), plan §5.4
> **Location**: `docs/python_binding_dev/spike/`

## Goal

Prove that Gluecodium's `Return<T, Error>` template (a hand-written value/error
tagged union, *not* an STL type) can be exposed to Python via a custom pybind11
`type_caster`, mapping:

- **success** → the inner value is returned to Python automatically;
- **failure** → a Python exception is raised carrying the error description.

## Approach

A single `type_caster<Return<Value, Error>>` specialization in `return_caster.h`:

1. On `has_value()` → delegates to `type_caster<Value>::cast(...)` (so `int`,
   `std::string`, `double`, etc. reuse pybind11's built-in casters).
2. On failure → `PyErr_SetString(PyExc_RuntimeError, msg)` then
   `throw pybind11::error_already_set()` so pybind11 propagates the real
   exception instead of wrapping a null handle as a generic `TypeError`.
3. `load()` returns `false` — `Return` is an output-only adapter (C++ → Python),
   never taken as a function argument.

A small traits helper `ReturnErrorToString<Error>` stringifies the error so the
same caster works for both `std::error_code` and user-defined error types. In the
real generator this would be specialized per error type to raise the matching
`py::exception<>` subclass (plan §5.4).

## Files

| File | Purpose |
|------|---------|
| `return_spike.h` | Standalone replica of Gluecodium's `Return<T, Error>` (same public API as `templates/cpp/common/Return.mustache`) |
| `return_caster.h` | The custom `type_caster` specialization |
| `spike_module.cpp` | pybind11 module exposing `divide`/`greet` (error_code) and `sqrt_safe` (custom error) |
| `test_spike.py` | 6 assertions: 3 success + 3 failure cases |
| `build.sh` | Compile + link + run |

## Build notes (important for the real generator)

- **Static Python gotcha**: the conda Python here is a *static* build
  (`Py_ENABLE_SHARED=0`, `libpython3.12.a`). Linking `libpython` into the
  extension creates a second interpreter copy → crash:
  `PyInterpreterState_Get: ... GIL is released`.
  **Fix**: link with `-undefined dynamic_lookup` so symbols resolve against the
  host interpreter at load time. `build.sh` auto-detects `Py_ENABLE_SHARED` and
  picks `-lpythonX.Y` vs `-undefined dynamic_lookup` accordingly.
- The `PYBIND11_TYPE_CASTER` macro needs a *simple* type name (it declares
  `type value;`), so a `using ReturnT = Return<Value, Error>;` alias is required
  — passing the template-id directly fails to parse.
- `cast()` must `throw pybind11::error_already_set()` after `PyErr_SetString`,
  not return a null `handle()`, otherwise pybind11 reports a misleading
  `TypeError: Unable to convert function return value`.

## Test results

```
PASS divide ok: returned 5
PASS divide by zero: raised RuntimeError: Argument list too long
PASS greet ok: returned 'hello, world'
PASS greet empty: raised RuntimeError: Invalid argument
PASS sqrt_safe ok: returned 9.0
PASS sqrt_safe neg: raised RuntimeError: MyError(-1)
ALL SPIKE CHECKS PASSED
```

## Conclusion

The `Return<T, Error>` caster is **feasible** and low-risk. The plan's Medium-risk
item is de-risked. For the real generator:

- Generate one `type_caster` (or per-error-type specialization) in
  `pybind11/_type_casters.h` (plan §6.1).
- Raise the generated `Error` subclass exception (not a bare `RuntimeError`) by
  specializing `ReturnErrorToString` / using `py::register_exception_translator`
  per error type.
- Reuse the `build.sh` link-flag detection logic in `cmake/modules/gluecodium/Python.cmake`
  (plan §7.4) so both shared and static Python builds work.
