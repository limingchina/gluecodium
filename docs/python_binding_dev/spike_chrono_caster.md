# Spike — `Date` / `Duration` pybind11 caster

> **Status**: ✅ Proven (compiles + runs on macOS/arm64, Python 3.12.3, pybind11 3.0.4)
> **Date**: 2026-07-12
> **Related**: `phase0_precheck.md` (last open Phase 0 item), plan §4.1 / §4.4
> **Location**: `docs/python_binding_dev/spike/`

## Goal

Confirm that the C++ types the Gluecodium C++ generator emits for LIME `Date` and
`Duration` are convertible to/from Python via `pybind11/chrono.h` (no hand-written
caster needed).

## Exact C++ types emitted (verified in source)

From `gluecodium/.../generator/cpp/CppNameResolver.kt`:

| LIME type | C++ type emitted | Source |
|-----------|------------------|--------|
| `Date` | `::std::chrono::system_clock::time_point` | `CppNameResolver.kt:168` |
| `Duration` | `::std::chrono::seconds` | `CppNameResolver.kt:169` |

> **Correction to plan §4.1**: the plan table lists `Duration` →
> `std::chrono::nanoseconds`. The actual generator emits **`std::chrono::seconds`**
> (the LIME `Duration` value's unit is resolved per-value in `resolveDurationValue`,
> but the canonical mapped type is `seconds`). `pybind11/chrono.h` handles both, so
> this does not change the conclusion — just note the real mapped type when writing
> the generator/templates.

## Approach

`#include <pybind11/chrono.h>` provides built-in casters for all standard
`std::chrono` types. No custom `type_caster` is required for `Date`/`Duration`:

- `std::chrono::system_clock::time_point` ↔ `datetime.datetime`
- `std::chrono::seconds` ↔ `datetime.timedelta`

## Files

| File | Purpose |
|------|---------|
| `chrono_spike.cpp` | pybind11 module exposing `get_epoch`/`add_days` (Date) and `make_duration`/`double_duration` (Duration) |
| `test_chrono.py` | 7 assertions covering both directions |
| `build_chrono.sh` | Compile + link + run (reuses the static/shared Python link detection from `spike_return_caster.md`) |

## Test results

```
PASS get_epoch is naive datetime
PASS get_epoch == 1970-01-01 local
PASS add_days +1 == 1970-01-02 local
PASS datetime arg accepted (returns datetime)
PASS make_duration is timedelta
PASS make_duration == 90s
PASS double_duration(30s) == 60s
ALL CHRONO SPIKE CHECKS PASSED
```

## Important behavior note (for the real generator)

`pybind11/chrono.h` converts `time_point` to a **naive `datetime.datetime` in
LOCAL time** — it does **not** attach `tzinfo`. On a UTC+1 machine the Unix epoch
appears as `1970-01-01 01:00`. If the Python API must expose timezone-aware UTC
datetimes (matching other Gluecodium platforms), a **custom `type_caster`** is
needed (plan §4.4 `Pybind11TypeCaster.mustache`) that:

- on `cast()`: converts `time_point` → `datetime(... , tzinfo=timezone.utc)`;
- on `load()`: accepts a `datetime.datetime` (naive or aware) → `time_point`.

`Duration` ↔ `timedelta` is fully automatic and needs no customization.

## Conclusion

The `Date`/`Duration` caster approach via `pybind11/chrono.h` is **feasible** and
low-risk. The plan's last open Phase 0 item is resolved. For the real generator:

- Add `#include <pybind11/chrono.h>` to the pybind11 binding files (alongside
  `<pybind11/stl.h>`).
- `Duration` works out of the box.
- `Date` works out of the box as a naive local datetime; if UTC-aware is required,
  implement the custom caster from plan §4.4.
