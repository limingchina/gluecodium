# Python binding implementation: review and improvement plan

> Resolution update (2026-10-05): all nine findings below have been fixed in separate signed-off commits on `python_bind`, published to PR #2. The final local Python 3.14 / pybind11 3.1.0 suite passed 446 tests; full Gradle had zero failures and 63 skips. The findings describe the original reviewed revision. See [fixes and validation](python-binding-fixes-progress.md) for commit IDs and before/fixed evidence.

## Executive assessment

Reviewed `python_bind` at `99abd74cf3e8275cdbf3603a86d84d0f926925c2` in `/workspace/gluecodium`, read-only. The implementation has substantial functional breadth and a working Python 3.10 native build. The separation between Kotlin model processing, generated wrapper modules, and pybind11 registrations is useful. The recent empty-stub fix is sound and the syntax regression test is valuable.

The passing suites establish substantial baseline behavior, but do not yet establish a consistent public Python type contract. Seven confirmed semantic/type-contract defects are listed below, alongside one high-priority threading risk and one documented lifecycle limitation. The most consequential themes are conversion consistency in both directions, identity independent of first access type, and stub fidelity. These are stronger priorities than adding more language features.

Baseline provided and previously independently checked: full Gradle suite 922 tests, zero failures, 63 skips; Python 3.10 functional suite 345 passed; 657 smoke `.py` and 458 `.pyi` files parse. This review used the existing Python 3.10.21/pybind11 3.1.0 functional extension and local mypy. Targeted probes below do not change repository sources or rebuild the extension. The current HEAD differs from the native build's earlier source commit; the reviewed runtime/template portions involved in these probes are unchanged, but this review is not a fresh native build of every HEAD file.

Severity: **High** means a potentially blocking runtime boundary defect requiring attention before claiming broader support; **Medium** means a reproducible incorrect API behavior or materially inaccurate typing contract; **Low** means a limited impact cleanup. Status explicitly distinguishes confirmed defects, known limitations, and unexecuted risks.

## Actionable findings

### 1. Medium — Overloaded wrappers accept `**kwargs` but discard them

**Status:** Confirmed defect; high confidence.

**Location:** `gluecodium/src/main/resources/templates/python/PythonFunction.mustache:26` and the native-call branches at lines 28–35. `PythonOverloadsValidator.kt:31` describes an `*args, **kwargs` dispatcher, but no generated overload call forwards `kwargs`.

**Reproduction:**

```python
import functional
from test.MethodOverloads import MethodOverloads
functional.test_MethodOverloads.is_boolean(input=True)  # True
MethodOverloads.is_boolean(input=True)                  # TypeError: incompatible function arguments
```

An even more subtle case is `ConstructorOverloads.create(input="text")`: the wrapper silently calls the zero-argument overload because the keyword was dropped. Existing `method_overloads_test.py` tests positional arguments only.

**Impact:** Valid Python calls fail or invoke a different overload; this violates the advertised dispatcher signature and generated named-parameter stubs.

**Fix:** Forward unwrapped keyword values in every overload branch, alongside positional arguments. Avoid implementing Python dispatch when native pybind11 keyword resolution already works. Separately ensure wrapper selection follows the chosen overload's return type, rather than assuming all overloads share the first overload's return shape.

**Verification:** Test static and instance overloads using keywords only and mixed positional/keyword arguments; include a zero-argument overload so lost keywords cannot accidentally pass. Check wrapper arguments inside keywords, bad keyword names, and duplicate arguments.

### 2. Medium — Cached wrappers can have the wrong public type, depending on call order

**Status:** Confirmed defect; high confidence.

**Location:** `PythonNativeBase.mustache:138`–143. The cache uses only a native pointer and returns the cached object without checking `wrapper_type`. Relevant generated factory methods originate in `PythonFunction.mustache:29`–31. `functional-tests/functional/input/lime/RefEquality.lime:38` defines both child and parent views of the singleton.

**Reproduction in a fresh Python process:**

```python
from test.DummyFactory import DummyFactory
from test.DummyChildClass import DummyChildClass
parent = DummyFactory.get_dummy_child_class_singleton_as_parent()
child = DummyFactory.get_dummy_child_class_singleton()
print(type(parent).__name__, type(child).__name__, parent is child)
# DummyParentClass DummyParentClass True
assert isinstance(child, DummyChildClass)  # fails
```

**Impact:** A method annotated as returning a child class returns its parent wrapper. Child-only methods may be missing, and behavior depends on which API was called first. Existing reference-equality tests verify same-type identity and distinct instances, not parent-first/child-first views.

**Fix:** Define the identity contract before changing the key. Ideally map native dynamic types to the most specific available public wrapper and cache that wrapper once. A `(pointer, wrapper_type)` key alone fixes type confusion but sacrifices identity across views; it must not be presented as a complete identity solution. Normalize base-subobject identity for multiple inheritance as part of the design.

**Verification:** Parent-first and child-first tests should agree on type and identity; cover classes, interfaces, multiple inheritance, and deliberately narrow interfaces. Preserve narrow-interface semantics documented in the interface template.

### 3. Medium — Nullable wrapper returns fail on cache misses

**Status:** Confirmed defect; high confidence.

**Location:** `PythonFunction.mustache:40`–42 passes the fully resolved return hint to `_get_or_create_wrapper`; `PythonNativeBase.mustache:142` invokes that hint as a constructor. `_wrap` at lines 103–105 handles unions, but the static wrapper path bypasses it.

**Reproduction:**

```python
import functional
from test.NullablePayload import NullablePayload
from test.NullableStatic import NullableStatic
value = NullablePayload(functional.test_NullablePayload.create())
NullableStatic.nullable_top_down_round_trip(value)
# TypeError: Cannot instantiate typing.Union
```

`None` succeeds; a native object already cached by `NullablePayload.create()` also succeeds. Those paths mask the failure.

**Impact:** Non-null values returned by nullable class/struct/interface factories can fail even though the matching nonnullable API works. The public signature claims `Optional[NullablePayload]`.

**Fix:** Route return conversion through the union-aware `_wrap`, or normalize optional hints to the actual wrapper type before cache lookup/construction. Keep `None` handling explicit.

**Verification:** Nullable return tests must include `None`, an existing cached object, and an uncached non-null native result; include optional structs, enums, interfaces, and collections containing optionals.

### 4. Medium — Callback boundaries expose native types and reject public wrappers

**Status:** Confirmed defect/implementation gap; high confidence. The workaround is explicitly recorded in contributor tests, but the user-facing type contract does not explain this split.

**Location:** `Pybind11TrampolineFunction.mustache:47`–50 uses `PYBIND11_OVERRIDE_PURE` directly with native values, without the wrapper conversions used by outbound Python methods. `functional-tests/functional/python/test/listeners_return_values_test.py:28`–30, 63–75 explicitly require native class/struct/enum results as a workaround.

**Incoming probe:** A `ForecastListener.on_forecast_data_provided` override receives dictionary values of type `functional.test_ForecastData`, and `isinstance(value, test.ForecastData.ForecastData)` is false, although its generated parameter annotation is `dict[str, ForecastData]`.

**Outgoing reproduction:**

```python
from test.ListenerWithReturn import ListenerWithReturn
from test.MessageDelivery import MessageDelivery
class Listener(ListenerWithReturn):
    def get_structured_message(self):
        return ListenerWithReturn.MessageStruct("Works")
MessageDelivery.create_me().get_structured_message(Listener())
# RuntimeError: Unable to cast Python instance ...MessageStruct to C++ type ...MessageStruct
```

**Impact:** User code following generated annotations and public wrapper imports fails in callbacks. Native values happen to expose similar fields, so current tests can pass without exercising the intended wrapper contract. The same boundary needs examination for lambdas and nested collections, rather than assuming named interface trampolines are the only affected path.

**Fix:** Add a consistent adapter around overrides: wrap native parameters into public types recursively; unwrap public return values before native casting. Use the identity policy from finding 2. Keep invocation/exception handling under the GIL, and avoid circular imports during module initialization by resolving wrapper adapters lazily.

**Verification:** Tests should use only public wrapper types in callback implementations, assert incoming `isinstance` and identity, and return structs/enums/classes/collections of wrappers. Exercise lambdas, property callbacks, nullable values, throwing methods, and callbacks invoked from C++, not direct Python override calls.

### 5. Medium — Mutable equatable structs violate Python's hash contract

**Status:** Confirmed defect; high confidence.

**Location:** `PythonStruct.mustache:34`–42 generates `__eq__` and `__hash__` for every equatable struct. `Pybind11Struct.mustache:64`–66 computes a value-based hash while generated setters remain available (`PythonField.mustache:31`).

**Reproduction:**

```python
from test.Equatable import Equatable
value = Equatable.EquatableStruct()
items = {value: "saved"}
old_hash = hash(value)
value.string_field = "changed"
assert hash(value) != old_hash  # observed
assert value not in items      # observed: key is still stored, lookup cannot find it
```

**Impact:** Dictionaries and sets can become inconsistent after mutation, including collections crossing the binding boundary. Existing equality tests do not test hashing or mutation after insertion.

**Fix:** Mutable value objects should normally be unhashable (`__hash__ = None`). Expose value hashing only when the full reachable value state is immutable. If LIME requires mutable structs as keys, define immutable snapshot/key adapters rather than silently offering an unstable hash. An identity hash cannot be combined with value equality as a shortcut.

**Verification:** Assert mutable structs raise `TypeError` when used as dict/set keys; immutable equatable structs must maintain equal hashes for equal values and stable hashes. Include nested mutable collections/structs inside nominally immutable outer structs.

### 6. Medium — Interface stubs erase inheritance and inherited API

**Status:** Confirmed typing defect; high confidence.

**Location:** `PythonStubInterface.mustache:22` emits `class Name:` unconditionally, unlike the class stub template. Generated `test/ChildInterface.pyi` imports `RootInterface` but does not use it as a base.

**Local mypy evidence:**

```python
from test.ChildInterface import ChildInterface
from test.RootInterface import RootInterface

def consume_root(value: RootInterface) -> None: ...
def consume_child(value: ChildInterface) -> None:
    consume_root(value)       # incompatible ChildInterface; expected RootInterface
    value.root_method("x")   # ChildInterface has no attribute root_method
```

The native pybind11 inheritance supports the corresponding inheritance relationship; the stub contract omits it.

**Impact:** Valid clients are rejected by static checking and inherited methods disappear from IDE completion. Syntax-only stub tests cannot detect this.

**Fix:** Emit public interface bases in the stubs, and use the same naming/import alias resolution as class bases. Do not automatically add those public Python bases to the runtime native-subclass hierarchy: pybind11 metaclass/MRO and native-versus-public inheritance need separate compatibility tests. If interfaces are intended to be structural protocols, adopt that deliberately across all related annotations rather than changing individual classes opportunistically.

**Verification:** Run a focused mypy or pyright consumer suite asserting interface substitution, inherited members, cross-package and multiple inheritance, and narrowing rules.

### 7. Medium — Struct stubs omit usable constructor signatures

**Status:** Confirmed typing defect; high confidence.

**Location:** `PythonStubStruct.mustache:22`–40 emits fields/functions/properties but no `__init__`, whereas runtime `PythonStruct.mustache:25`–32 accepts positional and keyword field construction through pybind11.

**Evidence:** `ForecastData(-2, 26)` is a supported runtime construction. Local mypy reports `Too many arguments for "ForecastData"` using the generated `.pyi`. This was the third error in the same focused consumer probe as finding 6.

**Impact:** Normal public value construction is rejected by type checkers. Missing constructor signatures also prevent useful autocomplete and checking of wrong field names/types.

**Fix:** Derive typed constructor overloads from the same struct constructor/default/accessor model used by `Pybind11StructInit`, including field constructors, defaults, excluded fields, immutable structs, and custom factories. Do not merely add untyped `*args, **kwargs`, which hides incorrect calls.

**Verification:** Positive and negative consumer checks for default construction, positional/keyword fields, named constructors, omitted defaults, skipped fields, external-accessor structs, nested structs, wrong types, and unknown field names.

### 8. High — GIL acquisition in trampolines does not establish safe synchronous threaded callbacks

**Status:** Source-backed risk; not executed on the functional module because the threaded feature is excluded. Confidence high in the potential deadlock mechanism, lower in application exposure without a representative enabled API.

**Location:** Native `.def` calls in `Pybind11Function.mustache:31` and throughout the template have no `gil_scoped_release`/`call_guard`; `Pybind11TrampolineFunction.mustache:36` acquires the GIL before entering a callback. `functional-tests/functional/input/src/cpp/ListenersThreads.cpp:62`–63 demonstrates the native worker-and-join pattern. `functional-tests/functional/CMakeLists.txt:374` excludes Python from `CallbacksWithThreads`.

**Failure mechanism:** Python calls a native method while holding the GIL; the method starts a worker and waits in `join`; the worker enters a generated trampoline and waits to acquire the GIL held by the waiting caller. Merely acquiring the GIL in each callback does not solve this cycle. Native long-running calls also block Python progress while retaining the GIL.

**Impact:** APIs that synchronously wait for worker-thread callbacks can hang. The guide's statement that trampolines acquire the GIL is correct but should not imply general threaded-callback support.

**Fix:** Establish a GIL policy for native calls and callbacks. Release the GIL only around native work, reacquiring before conversion that uses Python objects. Blanket call guards on every binding are unsafe for lambda bindings/custom conversions that call `py::cast` or `to_python_regular`; define typed boundaries and validate each category. Move acquisition after `m_impl` forwarding when no Python operations are involved if that forwarding can block. Define behavior for exceptions escaping callbacks and `noexcept` C++ overrides.

**Verification:** Enable a minimal worker-and-join case in a subprocess with a timeout; add detached interface and lambda callbacks, concurrent calls, retained/dropped callback references, and interpreter shutdown. A timeout protects CI and proves a hang is resolved. Do not claim this is already reproduced by the 345 tests.

### 9. Medium — Strong wrapper cache retains all returned shared objects until shutdown

**Status:** Confirmed, explicitly documented limitation, not a newly discovered undocumented regression.

**Location:** `PythonNativeBase.mustache:123` and 142–143; `docs/python_bindings.md:212`–213 documents the strong references. There is no per-instance removal path in the active Python cache.

**Probe:** Create a `DummyFactory.create_dummy_class()` wrapper, retain only `weakref.ref`, delete the caller's reference, and run `gc.collect()`: the weak reference remains live. Clear the cache and collect again: it becomes dead. This independently confirms wrapper/native retention.

**Impact:** Long-lived processes creating many native objects retain memory and any owned native resources (files, handles, threads) after application references disappear. This trades lifecycle correctness for identity stability.

**Fix:** Introduce a weak-value identity cache or an explicit lifecycle-aware cache, preserving strong references only where callback ownership needs them. Decide whether identity is required while a wrapper is alive or forever; the former allows weak caching. Audit trampoline lifetimes before removing strong ownership. Keep shutdown cleanup as a separate requirement.

**Verification:** Weak-reference/destructor tests with repeated allocation, identity while live, pointer reuse after destruction, listener retention rules, and subprocess shutdown. Test native resource release as well as Python object counts. Coordinate with finding 2; do not change cache keys and ownership independently.

## Architecture and maintainability

- **Conversion should have one contract.** Outbound functions, fields, properties, callbacks, lambdas, and static factories currently choose different conversion paths. The optional-return and callback defects are consequences of that duplication. Model conversion as explicit typed operations in Kotlin and render small reusable template fragments rather than branching repeatedly in `PythonFunction.mustache`.
- **Overload handling should be represented as a group.** Current `isFirstOverload` rendering selects one method's return hint for a generic dispatcher. Heterogeneous-return overloads are a credible unverified gap; add a dedicated generated fixture before deciding the fix. The validator checks C++ signature ambiguity, not all Python conversion ambiguity.
- **Stub generation needs the same API model as runtime generation.** Constructor and inheritance omissions cannot be fixed by parsing `.pyi` alone. Add a public consumer type-check suite. Cover omitted `-> None` on void methods and immutable-field annotations as part of that contract audit; these were inspected but not classified as separate findings.
- **Import planning currently handles direct mutual dependencies.** `PythonGenerator.kt:238`–245 looks for a reverse edge, not complete strongly connected components. Three-module cycles, nested aliases evaluated at runtime, and aliases involving inheritance deserve generated import-order tests. This is a code-backed coverage risk, not a reproduced failure in this review.
- **The generated C++ WrapperCache helper is inactive.** Searching Python templates found no `WrapperCache::instance` or `get_or_create` call sites; `_return_caster.h` merely includes its header. Its mutex/GIL/destruction concerns should not be attributed to the active Python cache as confirmed bugs. Remove unused infrastructure or connect it only through a clearly designed ownership policy.
- **Generator context is implicit.** Thread-local name/alias state in `PythonNameResolver` and map-based template data make rendering-order assumptions harder to inspect. Replace implicit state with an explicit immutable rendering context when doing conversion/import refactoring; avoid a broad rewrite before regression coverage exists.

## Build, packaging, errors, and documented limits

The current guide accurately describes several incomplete areas; they should be tracked as product improvements rather than reported as unexpected defects:

- `setup.py` is a starter: it lacks application/runtime sources, include paths, C++17 settings, wrapper discovery/data. The guide explicitly requires users to add them. A distributable package also needs a deliberate `Requires-Python >=3.10`, `.pyi` inclusion, and `py.typed`/PEP 561 policy. Existing functional tests copy files into `PYTHONPATH`; they do not validate wheel installation.
- The CMake helper requires pre-existing generated sources for the initial configure. Its comments describe glob-driven regeneration, but users should follow the guide's generation-before-configure requirement. The helper creates/links the extension; it does not install wrapper packages. Add a fresh build integration test instead of claiming one configure/build works automatically from an empty output directory.
- `functional-tests/scripts/python-env.sh:62` still accepts Python 3.8/3.9 and its diagnostics promise 3.8+, although CMake and the wrapper layer now require 3.10. This is a small but confirmed consistency issue: fail early with the correct requirement and update internal docs/AGENTS references together. No 3.8 interpreter was installed for this review.
- Enum-backed exception registry entries share `std::error_code`; last-registration/type/category ambiguity is explicitly documented (`docs/python_bindings.md:259`–261). Preserve the originating error category or generate per-call/per-exception translators before promising reliable exception selection for several enums.
- Payload exceptions currently expose messages rather than complete payload fields. Python exceptions raised inside throwing callbacks are not demonstrated to become native failed `Return` values; the caster's comments should not be taken as proof of that reverse error contract.
- Async/asyncio integration and package overrides are documented unsupported/inert. Narrow interfaces intentionally preserve only their declared view. Callback Python-object lifetime is explicitly assigned to the client. These are limits to retain in a support matrix, not errors invented by this review.
- Minimum declared pybind11 is 2.11, but this execution used 3.1.0. Compatibility with the minimum needs a separate matrix job. Python 3.13/3.14, free-threaded builds, Windows/macOS, multiple independent generated modules in one process, reload and subinterpreters were not validated.

## Coverage gaps and confidence

Current tests cover many primitives, collections, nullable basics, inherited method calls, external types, enum/constants, nested types, throwing methods, and synchronous listeners. The passing examples are useful, but some callback tests explicitly bypass public wrappers and some lambda tests call Python overrides directly or inspect aliases, so test names must not be interpreted as end-to-end native coverage of every annotated feature.

Add consumer contract tests for positional versus keyword behavior, return-shape dispatch, wrapper identity/type order, nullable cache misses, callback argument/return types, mutable hashing, and static typing. Add bounded subprocess tests for lifecycle/thread/shutdown behavior. Keep smoke comparisons and syntax parsing; augment them rather than replace them.

Confirmed probe results are high confidence for the exact fixtures. The thread, longer import-cycle, overload return-shape, and broader platform/interpreter observations are risks or missing verification, not falsely claimed reproduced bugs. I did not run sanitizers, rebuild the full native suite, produce/install a wheel, or install additional runtimes. No repository source changes, commits, publication, or network calls were performed by this reviewer.

## Prioritized improvement plan

### Near term: repair the public contract

1. **Add focused failing regressions first** for findings 1–7, using public wrappers. Split keyword forwarding, optional-return conversion, cache type selection, callback conversion, and hash behavior into reviewable changes. Each should prove the previously failing case and retain the 345 functional baseline.
2. **Fix keyword forwarding and optional hint normalization**; these are localized and can precede the ownership redesign. Add mixed kwargs/wrapper conversion checks and nullable uncached-return checks.
3. **Specify identity and lifecycle together**, then fix cached wrapper type selection. Choose dynamic wrapper selection and weak-cache semantics deliberately; add parent/child, multiple-inheritance, retention, and shutdown tests before replacing the cache. Callback conversion depends on this identity policy.
4. **Repair callback conversions** once the identity policy is stable. Cover structs/enums/classes and nested optionals/collections, then lambdas and callback properties. Replace test-only native-object workarounds with public API assertions.
5. **Make mutable equatable structs unhashable or define immutable key adapters**. Treat any affected struct-key API as a compatibility decision; verify immutable nesting before retaining value hashing.
6. **Emit constructor/inheritance-complete stubs** and establish a small mypy/pyright consumer gate. Update the 3.10 interpreter validator and docs together. Re-run generator/smoke tests, syntax validation, and native functional tests after each logical change.

**Scope/confidence:** Mostly localized runtime/template fixes plus explicit identity policy; high confidence in necessity and reproduction. Cache/callback changes require careful design and may expose additional lifecycle assumptions.

### Midterm: harden concurrency, packaging, and generator structure

1. **Define and test the GIL/error/ownership policy** with bounded worker-and-join and detached-callback subprocess tests before enabling Python `CallbacksWithThreads`. This depends on callback conversion and lifetime tests above.
2. **Test overload conversion and import graphs** with generated heterogeneous-return and three-module-cycle fixtures; move to overload-group rendering and SCC-based import planning only if the fixtures justify it.
3. **Provide one supported distribution workflow** (CMake install or wheel build) including generated runtime/implementation linking, Python ABI metadata, wrappers/stubs/typing markers, fresh generation and clean configuration. Test installing the artifact into an empty venv outside the build tree.
4. **Refactor conversion/template data into explicit typed plans** after regression coverage stabilizes; remove the unused C++ cache helper and consolidate repeated Kotlin type branching. Keep a small end-to-end sample for each boundary category.
5. **Expand the CI matrix** to declared minimum pybind11 and Python versions plus at least one second platform. Document tested versions separately from theoretical support.

**Scope/confidence:** Moderate-to-large changes; sequence tests and ownership policy before refactors. Packaging/concurrency improvements need focused prototypes, not only template snapshots.

### Long term: deliberate feature expansion

1. Extend error identity and payload preservation across multiple enum categories and callbacks; specify reverse error mapping before implementation.
2. Add async integration/package override behavior only after the public conversion contract is consistent, with explicit compatibility and naming rules.
3. Assess multi-module coexistence, subinterpreters/free-threaded Python, lifecycle at interpreter finalization, and performance of large recursive collections. State support explicitly; avoid claiming it from ordinary CPython tests.
4. Publish a maintained support matrix generated or checked against enabled functional features; retire historical development plans as the authoritative source of support claims.

**Scope/confidence:** Roadmap, not an approved implementation request. Dependencies are a stable runtime contract, real distribution tests, and bounded concurrency tests.

## Delivery gates

Near-term completion requires all seven confirmed defect regressions to pass, the existing native functional suite to remain green, fresh smoke outputs to match, all runtime/stub artifacts to parse, and the focused consumer type-check suite to pass. Cache/lifecycle work additionally requires weak-reference/destructor and process-shutdown checks; concurrency work requires a bounded threaded callback test and an explicit supported-feature declaration. Distribution work is complete only when a clean venv can import and exercise an installed artifact without build-tree PYTHONPATH. No feature should be marked complete solely from a template snapshot or alias-presence test.

## Reproduction setup

Runtime probes used:

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/workspace/python310-functional-build/functional:/workspace/python310-functional-build/functional/python \
/workspace/python310-venv/bin/python
```

Typing consumer fixture: `/workspace/python-review-typecheck.py`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/workspace/python-review-tools \
MYPYPATH=/workspace/python310-functional-build/functional \
/workspace/python310-venv/bin/python -m mypy \
  --cache-dir /workspace/python-review-mypy-cache --follow-imports=silent \
  /workspace/python-review-typecheck.py
```

Observed: exactly the three consumer errors described in findings 6–7. The generated package roots were selected explicitly so this check did not depend on packaging/PEP 561 discovery.
