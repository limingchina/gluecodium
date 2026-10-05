# Plan: Fix Functional Test Failures for Python Bindings

> **Date**: 2026-07-27
> **Branch**: `python_bind`
> **Status**: ✅ **COMPLETED** - All functional test failures resolved
> **Related**: [phase8_followup_plan.md](./phase8_followup_plan.md), [FunctionalTestFailures.txt](../../FunctionalTestFailures.txt)
> **Scope**: 19 failing pytest cases across 8 test files - **ALL FIXED**

---

## 1. Failure Summary - ✅ ALL RESOLVED

| # | Test File | Test Case | Error | Root Cause Group | Status |
|---|-----------|-----------|-------|-----------------|--------|
| 1 | `equatable_test.py` | `test_are_equal` | `TypeError: __init__() missing 1 required arg 'native'` | A (test drift) | ✅ FIXED |
| 2 | `equatable_test.py` | `test_not_equal` | Same | A (test drift) | ✅ FIXED |
| 3 | `equatable_test.py` | `test_struct_equality` | `assert a == b` fails | H (G13 struct eq) | ✅ FIXED |
| 4 | `exceptions_test.py` | `test_method_with_error_throws` | `functional.test_WithPayloadError: unknown error` | D (G7 exc type) | ✅ FIXED |
| 5 | `exceptions_test.py` | `test_method_with_payload_error_and_return_value` | Same | D (G7 exc type) | ✅ FIXED |
| 6 | `instance_in_struct_test.py` | `test_copy_instance_in_struct_from_method` | `NameError: 'InstanceInStructSelfHolder' is not defined` | C (B5 regression) | ✅ FIXED |
| 7 | `instance_in_struct_test.py` | `test_instance_in_not_null_struct` | Same | C (B5 regression) | ✅ FIXED |
| 8 | `lambdas_test.py` | `test_static_lambda_property` | `AttributeError: no attribute 'real_concatenator_set'` | E (G8 prop setter) | ✅ FIXED |
| 9 | `method_overloads_test.py` | `test_is_boolean_byte_list` | `RuntimeError: Unable to cast int to string` | F (G4 overload) | ✅ FIXED |
| 10 | `method_overloads_test.py` | `test_is_boolean_byte_set` | Same | F (G4 overload) | ✅ FIXED |
| 11 | `method_overloads_test.py` | `test_create_ulong` | `TypeError: 'int' object is not iterable` | F (G4 overload) | ✅ FIXED |
| 12 | `properties_test.py` | `test_readonly_attribute` | `TypeError: __init__() missing 1 required arg 'native'` | A (test drift) | ✅ FIXED |
| 13 | `properties_test.py` | `test_readwrite_attribute` | Same | A (test drift) | ✅ FIXED |
| 14 | `ref_equality_test.py` | `test_singleton_is_same_instance` | `assert first is second` fails | G (G13 wrapper cache) | ✅ FIXED |
| 15 | `ref_equality_test.py` | `test_round_trip_preserves_identity` | Same | G (G13 wrapper cache) | ✅ FIXED |
| 16 | `structs_immutable_test.py` | `test_create_all_types_immutable_struct` | `TypeError: unexpected keyword argument 'int8Field'` | B (G1 kwargs) | ✅ FIXED |
| 17 | `structs_immutable_test.py` | `test_nesting_immutable_struct` | Same | B (G1 kwargs) | ✅ FIXED |
| 18 | `structs_immutable_test.py` | `test_immutable_struct_field_is_readonly` | Same | B (G1 kwargs) | ✅ FIXED |
| 19 | `structs_immutable_test.py` | `test_immutable_struct_round_trip` | Same | B (G1 kwargs) | ✅ FIXED |

---

## 2. Root-Cause Groups & Mapping to Phase 8 Plan - ✅ ALL FIXED

| Group | Phase 8 Gap ID | Phase | Count | Complexity | Status |
|-------|--------------|-------|-------|------------|--------|
| **A** — Test/API drift (wrong constructor call in tests) | — | — | 4 | Trivial | ✅ FIXED |
| **B** — Struct `__init__` doesn't accept `**kwargs` | G1 | B1 | 4 | Small | ✅ FIXED |
| **C** — Missing deferred import in static method body | G1 | B5 (regression) | 2 | Small | ✅ FIXED |
| **D** — Native pybind11 exception ≠ Python exception class; error message SFINAE doesn't handle member fields | G7 | E3 (regression) | 2 | Medium | ✅ FIXED |
| **E** — Static property setter not emitted (lambda type) | G8 | G (partial) | 1 | Medium | ✅ FIXED |
| **F** — Overload dispatch fails for collection types | G4 | D3 (regression) | 3 | Large | ✅ FIXED |
| **G** — Wrapper cache not used in factory functions | G13 | I | 2 | Medium | ✅ FIXED |
| **H** — `@Equatable` structs lack `__eq__`/`__hash__` | G13 | I | 1 | Medium | ✅ FIXED |

---

## 3. Implementation Plan - ✅ ALL SPRINTS COMPLETED

> **All 5 sprints have been successfully completed, fixing all 19 functional test failures!**

### Sprint 1: Quick Wins (Group A, B, C) — 10 failures ✅ FIXED

#### Task A: Fix test/API drift (4 failures) ✅ FIXED

**Status**: ✅ **COMPLETED** - Updated test files to use correct factory methods

**Changes Made**:
- `equatable_test.py`: `EquatableClass()` → `EquatableClass.create("name")`
- `properties_test.py`: `Attributes()` → `Attributes.create()`

**Verification**: Both test files pass with 4 fewer failures.

---

#### Task B: Add `**kwargs` support to struct `__init__` (4 failures) ✅ FIXED

**Status**: ✅ **COMPLETED** - Updated PythonStruct.mustache to accept and forward `**kwargs`

**Changes Made**:
- Updated `PythonStruct.mustache` `__init__` to accept and forward `**kwargs`:
```python
def __init__(self, *args, **kwargs):
    if len(args) == 1 and not kwargs and isinstance(args[0], functional.test_...):
        super().__init__(args[0])
    else:
        super().__init__(functional.test_...(
            *[_unwrap(arg) for arg in args],
            **{k: _unwrap(v) for k, v in kwargs.items()}
        ))
```

**Verification**: `structs_immutable_test.py` passes with 4 fewer failures.

---

#### Task C: Add deferred import in static method bodies (2 failures) ✅ FIXED

**Status**: ✅ **COMPLETED** - Added deferred imports for circular dependencies in method bodies

**Changes Made**:
- Added `isAncestorReturnType` predicate to `PythonGeneratorPredicates.kt`
- Updated `PythonFunction.mustache` to emit deferred import when needed

**Verification**: `instance_in_struct_test.py` passes with 2 fewer failures.

---

### Sprint 2: Exception Handling Fix (Group D) — 2 failures ✅ FIXED

#### Task D: Fix exception type mismatch and error message (2 failures) ✅ FIXED

**Status**: ✅ **COMPLETED** - Fixed exception type bridging and SFINAE for member fields

**Changes Made**:
- Updated `Pybind11Exception.mustache` to set Python exception as base class
- Fixed `Pybind11ReturnCaster.mustache` SFINAE to handle member fields

**Verification**: `exceptions_test.py` passes with 2 fewer failures.

---

### Sprint 3: Lambda Property Setter (Group E) — 1 failure ✅ FIXED

#### Task E: Emit setter for static properties (1 failure) ✅ FIXED

**Status**: ✅ **COMPLETED** - Added static property setter generation

**Changes Made**:
- Updated `PythonProperty.mustache` to emit static property setters:
```mustache
{{#if isStatic}}
{{#ifPredicate "hasSetter"}}
    @staticmethod
    def {{resolveName}}_set(value{{#unless typeRef.isNullable}}: {{resolveName typeRef}}{{/unless}}):
{{#if setterComment}}        """{{resolveName setterComment}}"""
{{/if}}        {{nativeModule}}.{{typeName}}.{{resolveName}} = _unwrap(value, {{resolveName typeRef}})
{{/ifPredicate}}
{{/if}}
```

**Verification**: `lambdas_test.py::test_static_lambda_property` passes.

---

### Sprint 4: Overload Dispatch for Collections (Group F) — 3 failures ✅ FIXED

#### Task F: Fix overload resolution for collection-typed overloads (3 failures) ✅ FIXED

**Status**: ✅ **COMPLETED** - Implemented type-aware overload dispatch

**Changes Made**:
- Updated `PythonFunction.mustache` with type-checking dispatch logic
- Added predicates for overload type dispatch in `PythonGeneratorPredicates.kt`
- Implemented Python-side dispatch that inspects argument types

**Verification**: `method_overloads_test.py` passes with 3 fewer failures.

---

### Sprint 5: Referential Equality & Struct Equality (Group G, H) — 3 failures ✅ FIXED

#### Task G: Wire up wrapper cache in factory functions (2 failures) ✅ FIXED

**Status**: ✅ **COMPLETED** - Implemented Python-side wrapper cache

**Changes Made**:
- Added `_wrapper_cache` dict and `_get_or_create_wrapper` helper
- Updated `PythonFunction.mustache` to use wrapper cache for factory functions

**Verification**: `ref_equality_test.py` passes with 2 fewer failures.

---

#### Task H: Generate `__eq__`/`__hash__` for `@Equatable` structs (1 failure) ✅ FIXED

**Status**: ✅ **COMPLETED** - Added equality and hash methods for @Equatable structs

**Changes Made**:
- Added `isEquatable` predicate to `PythonGeneratorPredicates.kt`
- Updated `PythonStruct.mustache` to emit `__eq__` and `__hash__` methods
```python
def __eq__(self, other):
    if not isinstance(other, type(self)):
        return False
    return self._native == other._native

def __hash__(self):
    return hash(self._native)
```

**Verification**: `equatable_test.py::test_struct_equality` passes.

---

## 4. Completion Summary - ✅ ALL TASKS COMPLETED

> **All 5 sprints completed successfully! All 19 functional test failures have been resolved.**

### Final Status
- **Total Failures Fixed**: 19/19 ✅
- **Total Effort**: ~6-8 days (as estimated) ✅
- **All Tasks**: COMPLETED ✅

### Execution Timeline
```
Sprint 1 (Quick Wins) ─────────────────────────────────────────────────┐
  Task A (test fixes) ─── ✅ COMPLETED                                │
  Task B (struct kwargs) ─── ✅ COMPLETED                             │
  Task C (deferred import) ─── ✅ COMPLETED                           │
                                                                       ▼
Sprint 2 (Exception Fix) ─────────────────────────────────────────────┐
  Task D (exc type + message) ─── ✅ COMPLETED                        │
                                                                       ▼
Sprint 3 (Lambda Property) ───────────────────────────────────────────┐
  Task E (static prop setter) ─── ✅ COMPLETED                        │
                                                                       ▼
Sprint 4 (Overload Dispatch) ─────────────────────────────────────────┐
  Task F (collection overload) ─── ✅ COMPLETED                       │
                                                                       ▼
Sprint 5 (Equality & Cache) ───────────────────────────────────────────┐
  Task G (wrapper cache) ─── ✅ COMPLETED                             │
  Task H (struct __eq__) ─── ✅ COMPLETED                             │
                                                                       ▼
✅ SUCCESS: All 19 failures resolved
```

All tasks were **independent** and could be worked on in parallel, with the suggested order prioritizing the highest failure-count-per-effort tasks first.

---

## 5. Final Results

| Sprint | Tasks | Failures Fixed | Est. Effort | Status | Actual |
|--------|-------|----------------|-------------|--------|--------|
| 1 | A, B, C | 10 | ~1 day | ✅ COMPLETED | On schedule |
| 2 | D | 2 | ~1 day | ✅ COMPLETED | Completed |
| 3 | E | 1 | ~0.5 day | ✅ COMPLETED | Completed |
| 4 | F | 3 | ~2-3 days | ✅ COMPLETED | Completed |
| 5 | G, H | 3 | ~2 days | ✅ COMPLETED | Completed |
| **Total** | | **19** | **~6-8 days** | ✅ **ALL DONE** | **SUCCESS** |

**Key Achievements:**
- ✅ All 8 root-cause groups resolved
- ✅ All 19 individual test failures fixed
- ✅ No regressions introduced
- ✅ All Python functional tests now pass
- ✅ Sprint-based approach successful

---

## 6. Testing Strategy

> **Python environment**: Both `build-python-functional` and `run-python-tests` share
> Python detection logic via `scripts/python-env.sh`. It auto-detects a Python 3.8+
> interpreter with pybind11 installed by probing `python3` on `PATH`, common conda /
> miniconda / anaconda paths, Homebrew Python, and system Python — picking the first
> candidate that passes all checks. To override, pass `--python /path/to/python3` or
> set the `GLUECODIUM_PYTHON` environment variable. The detected interpreter's bin
> directory is prepended to `PATH` so that build and test always use the same Python,
> ensuring the pybind11 extension module's SOABI suffix matches.

For each task (run from the project root `gluecodium/`):

1. **Edit the generator template/source** (and test files for Task A).
2. **Force regeneration**: Touch a `.lime` input or `rm -rf functional-tests/build-python/functional/gluecodium` (see the stale-generated-code gotcha in AGENTS.md).
3. **Rebuild** (from `functional-tests/`):
   ```bash
   cd functional-tests && ./scripts/build-python-functional --publish
   ```
   This runs `publishToMavenLocal`, CMake configure/build, and CTest (which includes the
   full Python test suite) in one shot. The build script auto-detects the Python
   interpreter and pins it via `-DPython_EXECUTABLE`, so no manual `PATH` prefix is needed.
4. **Run a specific test file** (for iterative debugging):
   ```bash
   cd functional-tests && ./scripts/run-python-tests tests/<feature>_test.py -v
   ```
   This uses the same auto-detection to find the correct Python interpreter, sets
   `PYTHONPATH` to the build output directory, and forwards extra args (e.g. `-v`,
   `-k`, `--tb=short`) to pytest. Supports test-level targeting too:
   `tests/equatable_test.py::test_struct_equality`.
5. **Run smoke tests** to ensure no regressions in generated output:
   ```bash
   ./gradlew test
   ```
   These are Java/JUnit unit tests that compare generated code against reference files.
6. **Run all enabled Python functional tests** to check for cross-feature regressions:
   ```bash
   cd functional-tests && ./scripts/run-python-tests
   ```

---

## 7. Appendix: Affected Generator Files

| File | Tasks |
|------|-------|
| `templates/python/PythonStruct.mustache` | B (kwargs), H (__eq__) |
| `templates/python/PythonFunction.mustache` | C (deferred import), F (overload dispatch), G (wrapper cache) |
| `templates/python/PythonProperty.mustache` | E (static setter) |
| `templates/python/Pybind11Exception.mustache` | D (exc base class) |
| `templates/python/Pybind11ReturnCaster.mustache` | D (SFINAE fix) |
| `templates/python/Pybind11Struct.mustache` | H (eq operator binding) |
| `generator/python/PythonGeneratorPredicates.kt` | C, F, H (new predicates) |
| `functional-tests/.../python/test/equatable_test.py` | A (test fix) |
| `functional-tests/.../python/test/properties_test.py` | A (test fix) |

---

## 8. Phase 8 Plan Cross-Reference

| Task | Phase 8 Phase | Gap ID | Status in Phase 8 |
|------|--------------|--------|-------------------|
| A | — | — | Not in phase 8 (test drift) |
| B | B1 (StructsImmutable) | G1 | Phase B marked complete; this is a gap |
| C | B5 (InstanceInStruct) | G1 | Phase B5 marked complete; regression |
| D | E3 (Errors) | G7 | Phase E3 marked complete; regression |
| E | G (Lambdas) | G8 | Phase G in progress (G0 complete, G1 in progress) |
| F | D3 (MethodOverloading) | G4 | Phase D3 marked complete; regression |
| G | I1 (Equatable/RefEquality) | G13 | Phase I not started |
| H | I1 (Equatable/RefEquality) | G13 | Phase I not started |

**Key finding**: 3 of the 8 root-cause groups (B, C, D, F) are **regressions in features
marked as "complete"** in the phase 8 plan. These indicate that the phase 8 exit criteria
were met at the compile level but not at the runtime test level — the generated code compiles
but doesn't pass the functional tests. The remaining groups (E, G, H) correspond to phases
that are either in-progress (G) or not yet started (I).
