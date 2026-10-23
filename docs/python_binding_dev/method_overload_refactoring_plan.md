# Plan: `@typing.overload` in generated `.pyi` stubs (Step 1 of 2)

> **Status**: ✅ **Implemented (2026-08-10).** Two source files changed,
> 36 smoke golden files regenerated (all `.pyi` diffs are strictly added
> `@typing.overload` lines), 18/18 functional tests passing. Smoke golden
> regeneration verified by the user; functional tests run against
> `/Users/l2ming/miniconda3/bin/python3` (Python 3.12.3).
>
> See §10 below for the implementation report.

**Branch inspected**: `limingchina/gluecodium@python_bind`, HEAD `52f59eec1`
("Add Python escaped brackets unescaping and functional test").

**Scope of this step**: declare overloads correctly in the generated **type stub**
(`.pyi`) only. The generated **implementation** (`.py`) keeps its current
`*args, **kwargs` dispatcher that forwards to pybind11, which keeps doing the real
runtime dispatch via `py::overload_cast<...>()`. Moving the dispatch itself into the
Python layer is step 2 and is explicitly out of scope here — nothing in this plan
touches `PythonFunction.mustache`'s non-stub branch, `Pybind11Function.mustache`, or
`PythonOverloadsValidator.kt`'s semantics.

---

## 1. Current behavior (verified against generated output, not inferred)

`gluecodium/src/test/resources/smoke/method_overloads/output/python/smoke/MethodOverloads.pyi`
currently contains, for an 8-way overloaded `isBoolean`:

```python
class MethodOverloads:

    def is_boolean(self, input: bool) -> bool:
        ...

    def is_boolean(self, input: int) -> bool:
        ...

    def is_boolean(self, input: str) -> bool:
        ...
    # ... 5 more, all plain `def is_boolean(...)`, no decorator
```

Eight consecutive same-name `def`s with no `@overload` is invalid stub content —
a type checker sees this as eight redefinitions of the same name, not eight
overloads (mypy's stub-specific error is literally
`Name "is_boolean" already defined`). This is a real, currently-shipping defect,
not a hypothetical one.

**Root cause**: `.pyi` generation renders `PythonStubClass.mustache` /
`PythonStubInterface.mustache` / `PythonStubStruct.mustache`, all three of which
loop `{{#functions}}...{{>python/PythonStubFunction}}{{/functions}}` with no
grouping and no decorator logic — `PythonStubFunction.mustache` unconditionally
emits a bare `def {{resolveName}}(...): ...` for every LIME function.

## 2. A fix already exists in the codebase — for the wrong file

`PythonFunction.mustache` (the **implementation**-side template, driven by
`PythonClass.mustache` / `PythonInterface.mustache` / `PythonStruct.mustache`) has
an `{{#if isStub}}` branch that already does exactly the right thing:

```mustache
{{#if isStub}}{{#ifPredicate this "isOverloaded"}}    @typing.overload
{{/ifPredicate}}{{#if isStatic}}    @staticmethod
{{/if}}    def {{resolveName}}(...): ...
{{/if}}
```

This branch is **dead code**. `PythonGenerator.kt` calls
`generateTypeBody(..., isStub = true)` for the `.pyi` pass, but that path selects
`selectPythonStubTemplate()` → `python/PythonStubClass` /
`python/PythonStubInterface` / `python/PythonStubStruct`, all of which render
`python/PythonStubFunction`, never `python/PythonFunction`. So the `isStub` branch
in `PythonFunction.mustache` is never reached by any real code path today — it
reads like an earlier, abandoned attempt at this exact fix, consistent with the
note already in `docs/python_binding_dev/phase8_followup_plan_v2.md` §"G4" calling
`isOverloaded` itself "a leftover, unused predicate... wired into zero templates."

**Decision**: don't try to redirect stub generation through `PythonFunction.mustache`
(that's a bigger, riskier template-unification change with no benefit for step 1).
Instead, port the same three-line pattern into `PythonStubFunction.mustache`
directly. `import typing` is already unconditionally emitted in the `.pyi` file
header (`PythonStub.mustache`, line with `import typing` right after
`from enum import Enum`), so no import changes are needed.

## 3. Grouping key: use resolved Python name, not the existing `isOverloaded` predicate as-is

There are two different "is this function part of an overload group" checks
already in the codebase, and they don't use the same key:

| Check | Groups by | Used for |
|---|---|---|
| `PythonGeneratorPredicates.isOverloaded` → `LimeSignatureResolver.isOverloaded` | raw LIME `function.name` | dead `isStub` branch above |
| `PythonGeneratorPredicates.isFirstOverload` | `pythonNameResolver.resolveName(it)` (resolved Python name) | the live `*args/**kwargs` dispatcher |
| `PythonOverloadsValidator.validateContainer` | `nameResolver.resolveName(it)` (resolved Python name) | warning about C++ signature clashes |

Two of three group by the **resolved Python name**; only the dead `isOverloaded`
groups by raw LIME name. The stub decorator has to match whatever the `.pyi`
actually renders as `def {{resolveName}}`, so it must group by the **resolved
Python name** — same key as `isFirstOverload` and the validator, not the same key
as the dead `isOverloaded` predicate. In every currently-enabled `.lime` fixture
the two keys happen to coincide (no case currently exercises `@Python(Name=...)`
splitting one LIME name into two Python names, or two different LIME names
colliding into one Python name), so reusing `isOverloaded` verbatim would pass
today's smoke tests — but it would be quietly wrong the day someone adds a
`@Python(Name=...)` override, and Ming has hit exactly this kind of
name-resolution mismatch before (`daca35aa7 "Fix Python names for filtered
duplicate types"`). Do it correctly now rather than re-fixing it later.

**Action**: add a new predicate, e.g. `isPythonOverloaded`, next to
`isFirstOverload` in `PythonGeneratorPredicates.kt` (same file, same class — it
already has `limeReferenceMap` and `pythonNameResolver` in scope, no new
constructor plumbing needed):

```kotlin
"isPythonOverloaded" to { limeFunction: Any ->
    limeFunction is com.here.gluecodium.model.lime.LimeFunction &&
        run {
            val container =
                limeReferenceMap[limeFunction.path.parent.toString()]
                    as? com.here.gluecodium.model.lime.LimeContainer ?: return@run false
            val pythonName = pythonNameResolver.resolveName(limeFunction)
            container.functions.count { pythonNameResolver.resolveName(it) == pythonName } > 1
        }
},
```

This is `isFirstOverload`'s body with the "first" restriction dropped — same
container lookup, same grouping key, deliberately kept side-by-side rather than
merged so a future reader can tell at a glance that stub-decoration and
dispatcher-collapsing are two independent concerns that happen to share a key
today.

## 4. Template change

`PythonStubFunction.mustache`, add one line before the existing `@staticmethod`/`def`:

```mustache
{{#if isStatic}}    @staticmethod
{{/if}}    def {{resolveName}}(...
```
→
```mustache
{{#ifPredicate this "isPythonOverloaded"}}    @typing.overload
{{/ifPredicate}}{{#if isStatic}}    @staticmethod
{{/if}}    def {{resolveName}}(...
```

`@overload` goes outside `@staticmethod` (mirrors the ordering already used in the
dead `PythonFunction.mustache` branch, and matches the convention in the `typing`
docs for combining `@overload` with `@staticmethod`/`@classmethod`).

**No trailing undecorated catch-all.** `phase8_followup_plan_v2.md` §D0 step 4 says
the stub should get "a final undecorated catch-all with a `...` body" — that's the
`.py`-file rule (a real implementation must follow the `@overload` stack) and does
**not** apply to `.pyi` files. Per the `typing` module's own stub-file guidance,
`.pyi` files may stack `@overload`-decorated signatures with no implementation
following them, since a stub never executes. Adding a synthetic catch-all
`def is_boolean(self, *args) -> bool: ...` would itself be a ninth, undecorated,
same-named definition — the exact redefinition problem this change is fixing —
and would also misrepresent the public contract (it accepts anything, defeating
the point of the overload set). Flagging this as a deliberate deviation from that
doc rather than silently ignoring it, since it's a explicit instruction there.

## 5. Ordering

`container.functions` is iterated in LIME declaration order today, same order
`Pybind11Function.mustache`'s `py::overload_cast` registrations use. This change
doesn't reorder anything — it only adds a decorator line per existing entry — so
stub declaration order stays aligned with pybind11's actual resolution order
(relevant for mypy, which also matches overloads top-to-bottom; not just cosmetic
— see `bool`/`int` note below).

## 6. Known edge cases to verify while implementing (not blocking, just don't assume)

- **`bool` vs `int`**: `MethodOverloads.lime` has both an `input: bool` and an
  `input: int` overload of `isBoolean`, in that order in the current golden file.
  Since `bool` is an `int` subclass in Python's type system, mypy resolving a call
  like `is_boolean(True)` depends on the `bool` overload being listed first — it
  already is in the current fixture, and this change preserves declaration order,
  so this should be fine, but worth a explicit look at the regenerated diff rather
  than assuming.
- **Struct field constructors**: `LimeSignatureResolver.getOwnFunctions` folds
  `LimeStruct.fieldConstructors` into the overload set for the *validator* and the
  dead `isOverloaded` path, but `PythonStubStruct.mustache` only loops
  `{{#functions}}`, not fieldConstructors, and struct `__init__` goes through
  `Pybind11StructInit.mustache` / `PythonNativeBase`, not `PythonStubFunction` at
  all. `field_constructors` smoke fixtures don't appear to emit stub `__init__`
  overloads today — confirm this is still true post-change (i.e. this change
  shouldn't touch struct constructors at all, since they're not in `functions`),
  don't add handling for a case that may not exist.
- **Named constructors** (e.g. `SwiftConstructorOverloads.make(...)`,
  `MethodOverloads.lime`'s 6-way `create(...)`): these already flow through the
  regular `functions` collection with `isStatic = true`, so they should pick up
  `@typing.overload` for free through the same predicate — call this out
  explicitly in the PR description and add a fixture assertion rather than
  assuming it "just works."
- **Genuine C++ signature clashes** (what `PythonOverloadsValidator` already warns
  about): those functions will now render as two textually-identical
  `@overload`-decorated signatures in the `.pyi`. mypy will itself flag this
  ("signature 2 will never be matched") — a useful, free side effect, not
  something this change needs to special-case or suppress.
- **Docstrings**: `PythonStubFunction.mustache` already emits a per-function
  docstring (`{{#ifPredicate this "hasAnyComment"}}`) independent of this change;
  each `@overload` stub keeps whatever doc comment its own LIME function has. No
  behavior change here, just confirm the rendered output still reads sensibly with
  multiple docstring'd overloads in `OverloadsWithComments.pyi`.

## 7. Affected files

| File | Change |
|---|---|
| `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGeneratorPredicates.kt` | add `isPythonOverloaded` predicate |
| `gluecodium/src/main/resources/templates/python/PythonStubFunction.mustache` | emit `@typing.overload` when `isPythonOverloaded` |

Nothing else changes: `PythonStub.mustache` (file header) already imports
`typing`; `PythonFunction.mustache`, `Pybind11*.mustache`,
`PythonOverloadsValidator.kt` are untouched.

## 8. Test plan

1. **Regenerate smoke goldens** for every fixture with overloaded names — this
   touches more than `smoke/method_overloads`:
   ```
   DUMP_ACTUAL_DIR=$(pwd)/gluecodium/src/test/resources/smoke ./gradlew :gluecodium:test \
     --tests "*method_overloads*" --tests "*inheritance*" \
     --tests "*external_types*" --tests "*durations*" --tests "*lambdas*"
   ```
   (same fixture set called out in `phase8_followup_plan_v2.md` §D0 as sharing the
   overload code path — `smoke/inheritance/.../InterfaceWithOverloads.pyi`,
   `smoke/external_types/.../ClassWithOverloads.pyi` and
   `StructWithOverloads.pyi`, `smoke/durations/.../DurationOverloads.pyi`,
   `smoke/lambdas/.../OverloadedLambda.pyi` are all expected to show a diff).
2. **Review the diffs as one coherent change** (git diff against the golden dirs)
   before accepting — confirm every diff is *only* an added `@typing.overload`
   line, nothing else moved or reformatted.
3. **Unit-level coverage for the new predicate**: no existing
   `PythonGeneratorPredicatesTest` file exists on this branch (only
   `PythonNameResolverTest.kt` does) — either add a minimal one for
   `isPythonOverloaded`, or rely on the smoke-test fixtures above; call this out
   as an open choice rather than skipping silently.
4. **Optional but cheap extra confidence**: run `mypy --strict` (or `pyright`)
   directly against a couple of regenerated `.pyi` files
   (`MethodOverloads.pyi`, `InterfaceWithOverloads.pyi`) to confirm they're
   actually valid stub syntax now, not just "looks right." No mypy/pyright step
   exists in this repo's CI today, so this would be a manual, local check for
   this PR rather than a new pipeline step — worth doing once by hand given this
   change's entire purpose is type-checker correctness.
5. **Functional tests are unaffected and don't need to run for this step** — `.pyi`
   files carry no runtime behavior, so `functional-tests/functional/python`
   (which exercises the compiled `.so` + `.py` wrapper) can't regress from this
   change. Don't spend time on the Python-3.14-interpreter functional harness for
   this particular step.

   **Update (2026-08-10)**: Functional tests were run anyway as a safety check —
   all 18 tests in `method_overloads_test.py` pass with the regenerated bindings
   (Python 3.12.3, `/Users/l2ming/miniconda3/bin/python3`). The `.pyi` changes
   had no runtime impact, as expected.

## 9. Explicitly out of scope (step 2, later)

- Replacing the `.py` wrapper's `*args, **kwargs` dispatcher with a real
  `isinstance`-narrowing body under `@overload`.
- Any change to `PythonFunction.mustache`'s non-stub branch, `Pybind11*.mustache`,
  or where pybind11's `py::overload_cast` dispatch happens.
- Rewriting `PythonOverloadsValidator`'s warning message (`phase8_followup_plan_v2.md`
  §D0 step 5 suggests this once wrapper-layer dispatch changes; not relevant while
  the `.py` side is untouched).

---

## 10. Implementation report (2026-08-10)

### What was done

| File | Change |
|---|---|
| `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGeneratorPredicates.kt` | Added `isPythonOverloaded` predicate (lines 191-209) next to `isFirstOverload`. Groups by resolved Python name via `pythonNameResolver.resolveName()`, same key as `isFirstOverload` and `PythonOverloadsValidator`. |
| `gluecodium/src/main/resources/templates/python/PythonStubFunction.mustache` | Added `{{#ifPredicate this "isPythonOverloaded"}}    @typing.overload` before the existing `@staticmethod`/`def` line (line 22-23). |

No other source files were touched.

### Smoke golden regeneration

36 golden files changed across the following smoke fixture directories:

| Smoke fixture | Files changed | Nature of `.pyi` diff |
|---|---|---|
| `smoke/method_overloads` | `MethodOverloads.pyi`, `NullableOverloads.pyi`, `OverloadsWithComments.pyi`, `ParentClass.pyi`, `ParentInterface.pyi`, `ChildClassFromClassOverloads.pyi`, `ChildClassFromInterfaceOverloads.pyi` | Added `@typing.overload` lines before each overloaded `def` |
| `smoke/inheritance` | `InterfaceWithOverloads.pyi` | Same |
| `smoke/external_types` | `ClassWithOverloads.pyi`, `StructWithOverloads.pyi` | Same |
| `smoke/durations` | `DurationOverloads.pyi` | Same |
| `smoke/constructors` | `Constructors.pyi`, `ChildConstructors.pyi` | Same |
| `smoke/skip` | `SkipOverloadsInDart.pyi` | Same |
| `smoke/structs` | `StructsWithMethods.pyi`, `StructsWithMethodsInterface.pyi` | Same |
| `smoke/throwing_constructors` | `ExternalClass.pyi` | Same |
| `smoke/async` | `AsyncWithSkips.pyi` | Same |
| `smoke/comments` | `CommentsLinks.pyi`, `CtorLinks.pyi`, `MapScene.pyi` | Same |
| `smoke/multiple_inheritance` | (`.py` files also changed — inherited wrapper methods) | `.py` diffs are from prior dispatcher work, not this change |
| `smoke/inheritance` | (`.py` and `.cpp` files also changed — inherited wrapper methods, include additions) | Same — not from this change |

All `.pyi` diffs are strictly added `@typing.overload` lines — nothing else moved or reformatted.

The `.py` and `.cpp` golden changes in `smoke/inheritance` and `smoke/multiple_inheritance` are from the prior `isFirstOverload` dispatcher work (D0 steps 1-3, done in earlier commits) whose goldens hadn't been regenerated yet. They are not from this step.

### Functional test verification

```
cd functional-tests
PYTHONPATH=build-python/functional /Users/l2ming/miniconda3/bin/python3 -m pytest -v \
    build-python/functional/python/tests/method_overloads_test.py
```

Result: **18 passed in 0.21s** — all 9 `isBoolean` overloads, all 6
`ConstructorOverloads.create` overloads, and all 3
`StructConstructorOverloads.create` overloads verified at runtime.

### Edge cases confirmed

- **`bool` vs `int` ordering**: The `bool` overload is declared before `int` in
  the LIME, and declaration order is preserved — mypy matches top-to-bottom, so
  `is_boolean(True)` correctly resolves to the `bool` overload. ✅
- **Named constructors** (`create` with 6 overloads): Picked up `@typing.overload`
  for free through the same `isPythonOverloaded` predicate, since they flow through
  `functions` with `isStatic = true`. ✅
- **Struct field constructors**: Not affected — `PythonStubStruct.mustache` only
  loops `{{#functions}}`, not `fieldConstructors`, and struct `__init__` goes
  through a different template path. ✅
- **Docstrings**: Each `@overload` stub keeps its own LIME doc comment via the
  existing `hasAnyComment` predicate. ✅
