# Plan: Fix Functional Test Failures for Python Bindings

> **Date**: 2026-07-27
> **Branch**: `python_bind`
> **Status**: Planning
> **Related**: [phase8_followup_plan.md](./phase8_followup_plan.md), [FunctionalTestFailures.txt](../../FunctionalTestFailures.txt)
> **Scope**: 19 failing pytest cases across 8 test files

---

## 1. Failure Summary

| # | Test File | Test Case | Error | Root Cause Group |
|---|-----------|-----------|-------|-----------------|
| 1 | `equatable_test.py` | `test_are_equal` | `TypeError: __init__() missing 1 required arg 'native'` | A (test drift) |
| 2 | `equatable_test.py` | `test_not_equal` | Same | A (test drift) |
| 3 | `equatable_test.py` | `test_struct_equality` | `assert a == b` fails | H (G13 struct eq) |
| 4 | `exceptions_test.py` | `test_method_with_error_throws` | `functional.test_WithPayloadError: unknown error` | D (G7 exc type) |
| 5 | `exceptions_test.py` | `test_method_with_payload_error_and_return_value` | Same | D (G7 exc type) |
| 6 | `instance_in_struct_test.py` | `test_copy_instance_in_struct_from_method` | `NameError: 'InstanceInStructSelfHolder' is not defined` | C (B5 regression) |
| 7 | `instance_in_struct_test.py` | `test_instance_in_not_null_struct` | Same | C (B5 regression) |
| 8 | `lambdas_test.py` | `test_static_lambda_property` | `AttributeError: no attribute 'real_concatenator_set'` | E (G8 prop setter) |
| 9 | `method_overloads_test.py` | `test_is_boolean_byte_list` | `RuntimeError: Unable to cast int to string` | F (G4 overload) |
| 10 | `method_overloads_test.py` | `test_is_boolean_byte_set` | Same | F (G4 overload) |
| 11 | `method_overloads_test.py` | `test_create_ulong` | `TypeError: 'int' object is not iterable` | F (G4 overload) |
| 12 | `properties_test.py` | `test_readonly_attribute` | `TypeError: __init__() missing 1 required arg 'native'` | A (test drift) |
| 13 | `properties_test.py` | `test_readwrite_attribute` | Same | A (test drift) |
| 14 | `ref_equality_test.py` | `test_singleton_is_same_instance` | `assert first is second` fails | G (G13 wrapper cache) |
| 15 | `ref_equality_test.py` | `test_round_trip_preserves_identity` | Same | G (G13 wrapper cache) |
| 16 | `structs_immutable_test.py` | `test_create_all_types_immutable_struct` | `TypeError: unexpected keyword argument 'int8Field'` | B (G1 kwargs) |
| 17 | `structs_immutable_test.py` | `test_nesting_immutable_struct` | Same | B (G1 kwargs) |
| 18 | `structs_immutable_test.py` | `test_immutable_struct_field_is_readonly` | Same | B (G1 kwargs) |
| 19 | `structs_immutable_test.py` | `test_immutable_struct_round_trip` | Same | B (G1 kwargs) |

---

## 2. Root-Cause Groups & Mapping to Phase 8 Plan

| Group | Phase 8 Gap ID | Phase | Count | Complexity |
|-------|--------------|-------|-------|------------|
| **A** — Test/API drift (wrong constructor call in tests) | — | — | 4 | Trivial |
| **B** — Struct `__init__` doesn't accept `**kwargs` | G1 | B1 | 4 | Small |
| **C** — Missing deferred import in static method body | G1 | B5 (regression) | 2 | Small |
| **D** — Native pybind11 exception ≠ Python exception class; error message SFINAE doesn't handle member fields | G7 | E3 (regression) | 2 | Medium |
| **E** — Static property setter not emitted (lambda type) | G8 | G (partial) | 1 | Medium |
| **F** — Overload dispatch fails for collection types | G4 | D3 (regression) | 3 | Large |
| **G** — Wrapper cache not used in factory functions | G13 | I | 2 | Medium |
| **H** — `@Equatable` structs lack `__eq__`/`__hash__` | G13 | I | 1 | Medium |

---

## 3. Implementation Plan

### Sprint 1: Quick Wins (Group A, B, C) — 10 failures, ~1 day

#### Task A: Fix test/API drift (4 failures)

**Affected tests**: `equatable_test.py` (2), `properties_test.py` (2)

**Root cause**: Tests instantiate classes with `EquatableClass()` and `Attributes()` — no-arg
construction — but these classes only have factory constructors (`EquatableClass.create(name: String)`
and `Attributes.create()`). The generated Python `__init__(self, native)` requires a `native`
argument because these are non-trampoline classes (not open, no parents).

**Fix**: Update the test files to use factory methods:
- `equatable_test.py`: `EquatableClass()` → `EquatableClass.create("name")`
- `properties_test.py`: `Attributes()` → `Attributes.create()`

**Files to edit**:
- `functional-tests/functional/python/test/equatable_test.py`
- `functional-tests/functional/python/test/properties_test.py`

**Verification**: Run both test files, expect 4 fewer failures.

---

#### Task B: Add `**kwargs` support to struct `__init__` (4 failures)

**Affected tests**: `structs_immutable_test.py` (4)

**Root cause**: `PythonStruct.mustache` generates:
```python
def __init__(self, *args):
    if len(args) == 1 and isinstance(args[0], functional.test_...):
        super().__init__(args[0])
    else:
        super().__init__(functional.test_...(*[_unwrap(arg) for arg in args]))
```
This only accepts positional arguments. Immutable structs are constructed with keyword arguments
(`int8Field=0`, `pointField=point`, etc.) in the tests. The pybind11 native constructor already
supports keyword arguments (via `py::arg("...")`), but the Python wrapper doesn't forward `**kwargs`.

**Fix**: Update `PythonStruct.mustache` `__init__` to accept and forward `**kwargs`:
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

The `_unwrap` function already handles both basic types (returns as-is) and wrapper types
(extracts `_native`), so it works correctly for all field types passed as keyword arguments.

**Files to edit**:
- `gluecodium/src/main/resources/templates/python/PythonStruct.mustache`

**Verification**: Rebuild via `build-python-functional --publish` (touch a `.lime` input to
force regeneration), run `structs_immutable_test.py`, expect 4 fewer failures.

**Phase 8 reference**: B1 (`StructsImmutable`), Gap G1.

---

#### Task C: Add deferred import in static method bodies (2 failures)

**Affected tests**: `instance_in_struct_test.py` (2)

**Root cause**: The B5 circular-import fix added deferred imports in property getter bodies
(`from test.InstanceInStruct import InstanceInStruct` inside `my_self` getter in
`InstanceInStructSelfHolder.py`). However, static **method** bodies in `InstanceInStruct.py`
also reference `InstanceInStructSelfHolder` (the return-type wrapper) without a deferred import:

```python
# In InstanceInStruct.py:
@staticmethod
def create_in_struct() -> InstanceInStructSelfHolder:
    native_result = functional.test_InstanceInStruct.create_in_struct()
    return InstanceInStructSelfHolder(native_result)  # NameError!
```

The top-level `from test.InstanceInStructSelfHolder import InstanceInStructSelfHolder` was
**excluded** from the file's imports by the `isAncestorField`/circular-import logic, but the
deferred import was never added inside the method body.

**Fix**: The `PythonGenerator.kt` `generatePythonFile` method already handles `isAncestorField`
for property getters (adding deferred imports). The same pattern needs to be applied to
**function return types** — when a static method returns a type whose import was excluded due
to circular dependency, add a deferred `from <module> import <Type>` inside the method body.

This requires:
1. Adding a predicate like `isAncestorReturnType` (analogous to `isAncestorField`) that
   detects when a function's return type is one of its own container's ancestors.
2. Updating `PythonFunction.mustache` to emit a deferred import for the return type when
   `isAncestorReturnType` is true, just before the `return` statement.

**Files to edit**:
- `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGeneratorPredicates.kt` — add `isAncestorReturnType` predicate
- `gluecodium/src/main/resources/templates/python/PythonFunction.mustache` — emit deferred import when needed

**Alternative quick fix**: Add a `from __future__ import annotations` (already present) and
emit the return type as a string annotation. The runtime `return <Type>(native_result)` call
still needs the name in scope, so a deferred import inside the method body is still required.

**Verification**: Rebuild and run `instance_in_struct_test.py`, expect 2 fewer failures.

**Phase 8 reference**: B5 (`InstanceInStruct`), Gap G1. This is a regression in the B5 fix.

---

### Sprint 2: Exception Handling Fix (Group D) — 2 failures, ~1 day

#### Task D: Fix exception type mismatch and error message (2 failures)

**Affected tests**: `exceptions_test.py` (2)

**Root cause** (two issues):

**D1 — Exception type mismatch**: The native pybind11 raises `functional.test_WithPayloadError`
(a pybind11 `py::exception<Payload>` type registered in C++). The test expects
`WithPayloadError` (the Python class from `test/WithPayloadError.py`). These are different
types — `pytest.raises(WithPayloadError)` doesn't catch the native exception.

**D2 — Error message "unknown error"**: The `ReturnErrorToString` SFINAE in
`Pybind11ReturnCaster.mustache` checks for `decltype(std::declval<Error>().message())` —
i.e., a `message()` **method**. The `Payload` struct has a `message` **field** (not a method),
so `e.message()` is ill-formed, the SFINAE doesn't match, and it falls back to `"unknown error"`.

**Fix**:

For **D1**: Make the native pybind11 exception use the Python `WithPayloadError` class as its
base. Two approaches:
1. **Preferred**: In `Pybind11Exception.mustache`, after creating the `py::exception<...>`,
   set its base class to the Python `WithPayloadError` class (imported from the generated
   Python module). This way `isinstance(native_exc, WithPayloadError)` returns `True`.
2. **Alternative**: In the generated `Errors.py` wrapper, wrap the native call in a
   `try/except functional.test_WithPayloadError: raise WithPayloadError(...)` block.

For **D2**: Fix the `ReturnErrorToString` SFINAE to also handle member variables:
```cpp
// Handle member variable (field) named 'message'
template <typename Error, typename = void>
struct HasMessageMethod : std::false_type {};

template <typename Error>
struct HasMessageMethod<Error, std::void_t<decltype(std::declval<Error>().message())>> {
    static std::string convert(const Error& e) { return e.message(); }
};

// For Payload: access the 'message' field directly
template <typename Error, typename = void>
struct HasMessageField : std::false_type {};

template <typename Error>
struct HasMessageField<Error, std::void_t<decltype(std::declval<Error>().message)>> {
    static std::string convert(const Error& e) { return e.message; }
};
```
Or simpler: change the SFINAE to check `decltype(std::declval<Error>().message)` (without
parentheses) for member fields, and also handle methods.

Actually, the simplest fix for D2 is to change the SFINAE from `e.message()` to just `e.message`
(accessing the member, whether it's a method or a field, then calling it if it's a method):

```cpp
template <typename Error>
struct ReturnErrorToString<
    Error, std::void_t<decltype(std::declval<const Error&>().message)>> {
    static std::string convert(const Error& e) {
        if constexpr (std::is_invocable_v<decltype(&Error::message), const Error&>) {
            return e.message();
        } else {
            return e.message;
        }
    }
};
```

But this is complex. A simpler approach: since the `Payload` struct is a generated C++ struct
with a `message` field of type `std::string`, just access it directly:
```cpp
template <>
struct ReturnErrorToString<Payload> {
    static std::string convert(const Payload& e) { return e.message; }
};
```
But this requires per-type specialization, which the template can't do generically.

**Recommended approach for D1**: Register the Python exception class as the base of the
native pybind11 exception. In `Pybind11Exception.mustache`, after creating the exception,
set its base:
```cpp
void register_WithPayloadError(py::module_& module) {
    // Import the Python exception class
    py::object py_class = py::module_::import("test.WithPayloadError").attr("WithPayloadError");
    static py::exception<Payload> exc(module, "WithPayloadError", py_class);
    ...
}
```

**Files to edit**:
- `gluecodium/src/main/resources/templates/python/Pybind11Exception.mustache` — set Python base class
- `gluecodium/src/main/resources/templates/python/Pybind11ReturnCaster.mustache` — fix SFINAE for member fields

**Verification**: Rebuild and run `exceptions_test.py`, expect 2 fewer failures.

**Phase 8 reference**: E3 (`Errors`), Gap G7. This is a regression in the E3 fix.

---

### Sprint 3: Lambda Property Setter (Group E) — 1 failure, ~0.5 day

#### Task E: Emit setter for static properties (1 failure)

**Affected tests**: `lambdas_test.py` (1)

**Root cause**: `PythonProperty.mustache` only emits a setter for **non-static** properties
(the `{{#ifPredicate "hasSetter"}}` block is inside the `{{#unless isStatic}}` branch).
Static properties with `{ get set }` (like `Lambdas.realConcatenator`) only get a getter.

The test calls `Lambdas.real_concatenator_set(lambda first, second: ...)`, but the generated
code only has `Lambdas.real_concatenator()` (getter).

**Fix**: Add a static property setter branch in `PythonProperty.mustache`. After the
`{{#if isStatic}}` getter block, add:
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

Note: The test uses `real_concatenator_set` naming convention (property name + `_set` suffix)
for the static setter, matching how non-static properties use `@property.setter`. For static
properties, Python doesn't have a native `@property` mechanism, so the convention is a
`<name>_set` static method.

**Files to edit**:
- `gluecodium/src/main/resources/templates/python/PythonProperty.mustache`

**Verification**: Rebuild and run `lambdas_test.py::test_static_lambda_property`, expect 1
fewer failure.

**Phase 8 reference**: Phase G (Lambdas), Gap G8. Partial — only the static property setter
part; the rest of Phase G (lambda function parameters/returns) is separate.

---

### Sprint 4: Overload Dispatch for Collections (Group F) — 3 failures, ~2-3 days

#### Task F: Fix overload resolution for collection-typed overloads (3 failures)

**Affected tests**: `method_overloads_test.py` (3)

**Root cause**: The Python wrapper for overloaded methods uses `*args, **kwargs` dispatch:
```python
@staticmethod
def is_boolean(*args, **kwargs) -> bool:
    return functional.test_MethodOverloads.is_boolean(*[_unwrap(a) for a in args])
```

This delegates to the native pybind11 function, which has multiple overloads registered via
`py::overload_cast`. When `[1, 2, 3]` is passed, pybind11 tries overloads in registration
order. If `isBoolean(List<String>)` is tried before `isBoolean(List<Byte>)`, pybind11
attempts to cast `1` (int) to `std::string`, fails, and throws a `RuntimeError` instead of
trying the next overload.

Similarly, `create(42)` fails because pybind11 tries the `List<Double>` overload and fails
with `'int' object is not iterable`.

**Fix** (two approaches):

**F1 — Python-side type dispatch** (recommended for immediate fix): Generate explicit
type-checking dispatch code in the Python wrapper that inspects argument types and calls the
correct native overload. For each overloaded method, emit a dispatch function:
```python
@staticmethod
def is_boolean(*args) -> bool:
    if len(args) == 1:
        arg = args[0]
        if isinstance(arg, bool):
            return functional.test_MethodOverloads.is_boolean(_unwrap(arg, bool))
        if isinstance(arg, int):
            return functional.test_MethodOverloads.is_boolean(_unwrap(arg, int))
        if isinstance(arg, str):
            return functional.test_MethodOverloads.is_boolean(_unwrap(arg, str))
        if isinstance(arg, MethodOverloadsPoint):
            return functional.test_MethodOverloads.is_boolean(_unwrap(arg, MethodOverloadsPoint))
        if isinstance(arg, list):
            # Check element types to disambiguate List<String> vs List<Byte>
            if all(isinstance(x, str) for x in arg):
                return functional.test_MethodOverloads.is_boolean(_unwrap(arg, list[str]))
            if all(isinstance(x, int) for x in arg):
                return functional.test_MethodOverloads.is_boolean(_unwrap(arg, list[int]))
        if isinstance(arg, (set, frozenset)):
            ...
    elif len(args) == 4:
        ...
    # Fallback: try all overloads
    return functional.test_MethodOverloads.is_boolean(*[_unwrap(a) for a in args])
```

This requires updating `PythonFunction.mustache` to emit type-checking dispatch code for
overloaded methods, using the parameter type information from the LIME model.

**F2 — C++-side overload priority** (alternative): Reorder the pybind11 overload
registrations so that more specific overloads (e.g., `List<Byte>`) are tried before more
general ones (e.g., `List<String>`). However, pybind11's overload resolution doesn't
guarantee a "try next on failure" behavior — it typically fails on the first attempted cast.

**Files to edit (F1 approach)**:
- `gluecodium/src/main/resources/templates/python/PythonFunction.mustache` — add type-checking dispatch for overloaded methods
- `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGeneratorPredicates.kt` — add predicates for type dispatch

**Verification**: Rebuild and run `method_overloads_test.py`, expect 3 fewer failures.

**Phase 8 reference**: D3 (`MethodOverloading`), Gap G4. This is a regression in the D3 fix.

---

### Sprint 5: Referential Equality & Struct Equality (Group G, H) — 3 failures, ~2 days

#### Task G: Wire up wrapper cache in factory functions (2 failures)

**Affected tests**: `ref_equality_test.py` (2)

**Root cause**: The `WrapperCache` C++ class exists (`Pybind11WrapperCache.mustache`) but is
not used in the generated factory function code. Each call to
`DummyFactory.get_dummy_class_singleton()` creates a new `DummyClass(native_result)` Python
wrapper, even though the native singleton returns the same C++ instance. The Python `is`
operator checks object identity, so two different wrapper objects are not `is`-equal.

The generated factory code:
```python
@staticmethod
def get_dummy_class_singleton() -> DummyClass:
    native_result = functional.test_DummyFactory.get_dummy_class_singleton()
    return DummyClass(native_result)  # Always creates a new wrapper
```

**Fix**: Use the wrapper cache in factory functions that return wrapper types. The generated
factory function should:
1. Get the native result
2. Extract the C++ pointer from the native result
3. Call `WrapperCache::instance().get_or_create(ptr, [&]() { return DummyClass(native_result); })`
4. Return the cached or newly-created wrapper

This can be done either in:
- **C++ side (Pybind11Function.mustache)**: Wrap the native call in a lambda that uses the
  wrapper cache. Requires detecting which functions return a wrapper type (class/interface).
- **Python side (PythonFunction.mustache)**: After getting the native result, check a Python
  wrapper cache (a dict mapping `id(native_result)` → wrapper) before creating a new wrapper.

**Recommended approach**: Python-side wrapper cache, since it's simpler and doesn't require
modifying C++ binding code. Add a `_wrapper_cache` dict in `_native_base.py` and a helper
function `_get_or_create_wrapper(native, wrapper_type)` that checks the cache:
```python
_wrapper_cache = {}

def _get_or_create_wrapper(native, wrapper_type):
    if native is None:
        return None
    key = (id(native), wrapper_type)
    cached = _wrapper_cache.get(key)
    if cached is not None:
        return cached
    wrapper = wrapper_type(native)
    _wrapper_cache[key] = wrapper
    return wrapper
```

Then update `PythonFunction.mustache` to use `_get_or_create_wrapper(native_result, <ReturnType>)`
instead of `<ReturnType>(native_result)` for factory functions returning wrapper types.

**Files to edit**:
- `functional-tests/.../_native_base.py` (generated from template, check source) — add wrapper cache
- `gluecodium/src/main/resources/templates/python/PythonFunction.mustache` — use wrapper cache for wrapper return types

**Verification**: Rebuild and run `ref_equality_test.py`, expect 2 fewer failures.

**Phase 8 reference**: Phase I (I1 — `Equatable`/`RefEquality`), Gap G13.

---

#### Task H: Generate `__eq__`/`__hash__` for `@Equatable` structs (1 failure)

**Affected tests**: `equatable_test.py` (1 — `test_struct_equality`)

**Root cause**: `@Equatable` structs should generate `__eq__` and `__hash__` methods that
delegate to the C++ equality operator. Currently `PythonStruct.mustache` doesn't emit these
methods. The test `assert a == b` fails because the default `__eq__` (identity comparison)
returns `False` for two distinct struct instances with the same field values.

**Fix**: In `PythonStruct.mustache`, when the struct has the `@Equatable` attribute, emit:
```python
def __eq__(self, other):
    if not isinstance(other, type(self)):
        return False
    return self._native == other._native

def __hash__(self):
    return hash(self._native)
```

The C++ struct already has `operator==` and `std::hash` generated by the C++ generator for
`@Equatable` types, so pybind11 will expose them through the native object.

This requires:
1. Adding an `isEquatable` predicate to `PythonGeneratorPredicates.kt` (checking for
   `LimeAttributeType.EQUATABLE` on the struct).
2. Updating `PythonStruct.mustache` to emit `__eq__` and `__hash__` when `isEquatable` is true.
3. Ensuring the pybind11 binding registers `__eq__` (either via `def("__eq__", ...)` or via
   pybind11's automatic operator support).

**Files to edit**:
- `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGeneratorPredicates.kt` — add `isEquatable` predicate
- `gluecodium/src/main/resources/templates/python/PythonStruct.mustache` — emit `__eq__`/`__hash__`
- Possibly `gluecodium/src/main/resources/templates/python/Pybind11Struct.mustache` — register equality operator

**Verification**: Rebuild and run `equatable_test.py::test_struct_equality`, expect 1 fewer
failure.

**Phase 8 reference**: Phase I (I1 — `Equatable`), Gap G13.

---

## 4. Execution Order & Dependencies

```
Sprint 1 (Quick Wins) ─────────────────────────────────────────────────┐
  Task A (test fixes) ─── no deps, do first                            │
  Task B (struct kwargs) ─── no deps, parallel with A                  │
  Task C (deferred import) ─── no deps, parallel with A/B               │
                                                                       ▼
Sprint 2 (Exception Fix) ─────────────────────────────────────────────┐
  Task D (exc type + message) ─── no deps                              │
                                                                       ▼
Sprint 3 (Lambda Property) ───────────────────────────────────────────┐
  Task E (static prop setter) ─── no deps                              │
                                                                       ▼
Sprint 4 (Overload Dispatch) ─────────────────────────────────────────┐
  Task F (collection overload) ─── no deps                             │
                                                                       ▼
Sprint 5 (Equality & Cache) ───────────────────────────────────────────┐
  Task G (wrapper cache) ─── no deps                                   │
  Task H (struct __eq__) ─── no deps, parallel with G                  │
                                                                       ▼
Done: All 19 failures resolved
```

All tasks are **independent** — no task depends on another. They can be worked on in
parallel, but the suggested order prioritizes the highest failure-count-per-effort tasks
first.

---

## 5. Effort Estimates

| Sprint | Tasks | Failures Fixed | Est. Effort | Risk |
|--------|-------|----------------|-------------|------|
| 1 | A, B, C | 10 | ~1 day | Low — template/test fixes |
| 2 | D | 2 | ~1 day | Medium — exception type bridging |
| 3 | E | 1 | ~0.5 day | Low — template addition |
| 4 | F | 3 | ~2-3 days | **High** — overload dispatch redesign |
| 5 | G, H | 3 | ~2 days | Medium — wrapper cache + equality |
| **Total** | | **19** | **~6-8 days** | |

---

## 6. Testing Strategy

For each task:

1. **Edit the generator template/source** (and test files for Task A).
2. **Force regeneration**: Touch a `.lime` input or `rm -rf functional-tests/build-python/functional/gluecodium` (see the stale-generated-code gotcha in AGENTS.md).
3. **Rebuild**: `cd functional-tests && ./scripts/build-python-functional --publish`
4. **Run the specific test file**:
   ```bash
   cd build-python/functional/python
   PYTHONPATH=".../build-python/functional" python3 -m pytest tests/<feature>_test.py -v
   ```
5. **Run smoke tests** to ensure no regressions:
   ```bash
   ./gradlew test
   ```
6. **Run all enabled Python functional tests** to check for cross-feature regressions:
   ```bash
   cd build-python/functional/python
   PYTHONPATH=".../build-python/functional" python3 -m pytest -v
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
