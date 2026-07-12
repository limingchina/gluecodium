# Phase 0 — Prerequisites Precheck

> **Status**: Completed
> **Date**: 2026-07-12
> **Source plan**: `docs/python_pybind11_plan.md` (Phase 0, lines 52–62)
> **Scope**: Verify pybind11 version/dependencies and C++ generator compatibility before starting implementation.

---

## 0.1 pybind11 version and dependencies

| Check | Result | Status |
|-------|--------|--------|
| Python interpreter | `Python 3.12.3` (conda env at `/Users/l2ming/miniconda3/bin/python3`) | ✅ ≥ 3.8 |
| pybind11 installed | **Installed**: version **3.0.4** (include dir `/Users/l2ming/miniconda3/lib/python3.12/site-packages/pybind11/include`) | ✅ |
| pybind11 installable | `pip3 install pybind11` resolves to **3.0.4** (≥ 2.11.0 required) | ✅ |
| Target platforms | macOS (clang) confirmed; Linux/Windows to be validated in CI | ⏳ |

**Dependency status**: pybind11 **3.0.4** is now installed in the active conda env
(`/Users/l2ming/miniconda3/bin/python3`). The plan's minimum pin of `2.11.0` is satisfied.
CMake integration (plan §7.4) should use `find_package(pybind11 REQUIRED)`; the include
directory is discoverable via `pybind11::pybind11` / `pybind11_get_include()`.

---

## 0.2 C++ generator compatibility

| Check | Result | Status |
|-------|--------|--------|
| Headers includable by pybind11 | C++ headers use `#pragma once` and are self-contained (e.g. `CppHeader.mustache:23`, `Return.mustache:41`) | ✅ |
| `std::optional<T>` | Emitted via `CppNameResolver.kt:124` → `std::optional<...>` | ✅ pybind11/stl.h |
| `std::vector<T>` | Emitted via `CppNameResolver.kt:256` | ✅ pybind11/stl.h |
| `std::unordered_map<K,V>` | Emitted via `CppNameResolver.kt:262` | ✅ pybind11/stl.h |
| `std::unordered_set<T>` | Emitted via `CppNameResolver.kt:267` | ✅ pybind11/stl.h |
| `Return<T, Error>` exception mapping | Custom template class (`Return.mustache`); API: `has_value()`, `error()`, `unsafe_value()`, `safe_value()`, `operator bool`. **Not** a standard STL/pybind11 type | ✅ **Spike proven** — see `spike_return_caster.md` |

### Evidence

- **`Return<T, Error>` definition**: `gluecodium/src/main/resources/templates/cpp/common/Return.mustache`
  - `template < class Value, class Error = std::error_code > class Return`
  - Public API: `explicit operator bool() const`, `bool has_value() const`, `Error error() const`, `Value unsafe_value()`, `Value safe_value()`.
  - Internal representation is a tagged union (`m_has_value` + `m_value`/`m_error`), so it cannot be auto-converted by pybind11.
- **LIME model**: `lime-runtime/.../model/lime/LimeReturnType.kt` — `class LimeReturnType(val typeRef: LimeTypeRef, ...)`.
- **C++ emission**: `gluecodium/src/main/resources/templates/cpp/CppReturnType.mustache` emits
  `::Return< value, error >` (or `::std::error_code` when the error type is an enumeration).

---

## Key findings & risks

1. **`Return<T, Error>` — was the only hard blocker** (plan Risk table, "Medium"). It is a
   hand-written template (value/error union) with no pybind11 equivalent. **Spike completed 2026-07-12**:
   a custom `type_caster` was prototyped, compiled, and run successfully
   (see `spike_return_caster.md`). Success → inner value returned; failure → `RuntimeError`
   carrying the error message. **De-risked.**
2. **All STL containers map automatically** once `#include <pybind11/stl.h>` is added — no custom
   casters needed for `optional`/`vector`/`map`/`set`.
3. **`Date`/`Duration`/`Locale`** (per plan §4.1) still need custom casters via `pybind11/chrono.h` +
   `Locale` — these are separate from `Return` and can follow the same pattern.
4. **pybind11 is not yet a build dependency** — `cmake/modules/gluecodium/Python.cmake` (plan §7.4) and
   `find_package(pybind11 REQUIRED)` need to be added before any functional test compiles.

---

## Recommended next steps

- [x] Install pybind11 (`pip3 install pybind11`) — **done**, version 3.0.4.
- [x] **Spike**: prototype a `Return<T, Error>` type_caster — **done**, compiles & passes all 6 checks
      (see `spike_return_caster.md`). De-risks the Medium-impact item before M2.
- [ ] Confirm `Date`/`Duration` caster approach via `pybind11/chrono.h` (separate from `Return`).

---

## Precheck verdict

**GREEN** — all Phase 0 items resolved. pybind11 3.0.4 installed; C++ headers are includable; STL
containers map automatically; and the `Return<T, Error>` caster spike is proven. No blockers remain for
starting Phase 1 (LIME model layer extensions).
