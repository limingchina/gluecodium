# Phase 8 Follow-up: Re-enabling Narrowed Functional Features for Python (v2)

> **Date**: 2026-07-20 (updated 2026-08-10) **Branch**: `python_bind` **Status**: Active follow-up; Phase A (A1-A7) and Phase C (C1-C4) complete; Phase D0 step 4 (`.pyi` stub `@typing.overload`) complete; Phase D root cause re-diagnosed **Supersedes**: `phase8_followup_plan.md` (2026-07-18) — that document remains useful for Phase A/B/C history but its Phase D-K status no longer matches the codebase. **Related**: [phase8_status.md](./phase8_status.md), [python_pybind11_plan.md](../python_pybind11_plan.md), [method_overload_refactoring_plan.md](./method_overload_refactoring_plan.md)
>
> **⚠️ Gotcha — stale generated code after a generator change (carried over from v1, still applies):** the CMake custom command that invokes Gradle for code generation depends only on the LimeIDL inputs and options file, not on the published Gluecodium jar. If you edit a template or generator Kotlin source, re-publish, and rebuild **without touching a `.lime` input**, generation is skipped and you'll silently test stale output. Always touch a relevant `.lime` file or `rm -rf functional-tests/build-python/functional/gluecodium` before rebuilding, and verify the regenerated file actually changed before concluding a fix failed or succeeded.

---

## 0. What changed since the 2026-07-18 revision

A pass over the actual `python_bind` checkout (source, generated smoke goldens, and `functional/CMakeLists.txt`) turned up three things that materially change the plan:

1. **`functional/CMakeLists.txt` already lists `python` for `Inheritance` (D1), `MultipleInheritance` (D2), `MethodOverloading` (D3), `ExternalTypes` (E1), and `Errors` (E3)** — i.e. generation is already turned on for all of Phase D and half of Phase E, despite the plan describing them as blocked behind Phase C. These are enabled-but-failing, not not-yet-started.
2. **G3 (trampoline doesn't override inherited pure-virtuals) is already fixed.** Both `Pybind11Class.mustache` and `Pybind11Interface.mustache` already iterate `{{#inheritedFunctions}}` in their trampoline sections — this is exactly the fix D1 originally called for. It most likely landed as a side effect of the C1 (`Properties`) trampoline work, whose status notes already mention trampoline overrides using `PYBIND11_OVERRIDE_PURE`.
3. **G4 (Python doesn't support overloaded method names) is *half*-fixed, and the plan's remaining description of it was wrong about which half.** `Pybind11Function.mustache` already emits `py::overload_cast<...>()` correctly, gated by an `isCppOverloaded` predicate that walks own **and inherited** functions — this part works today and is verified against generated smoke output. The actual break is one layer up, in the generated **Python wrapper class**: `PythonClass.mustache`/`PythonInterface.mustache` emit one `def <name>(...)` per Lime function with no de-duplication, so in any overload group only the *last*-declared Lime function's wrapper method survives in the class body — the rest are silently shadowed. Confirmed directly against golden output (see §2.4).

Because `Inheritance.lime` (`getData`), `MultipleInheritance.lime` (`parentFunction`, `childFunction`), `Errors.lime` (`methodWithError`), and `ExternalTypes.lime` (`allOverloadsExposed`, `some_Method`) all contain overloaded names, **this single wrapper-layer bug is very likely the shared blocker for D1, D2, D3, E1, and E3 simultaneously.** Phase D has been restructured below so the cross-cutting fix (now D0) lands before the per-feature verification tasks (D1-D3), instead of being buried inside D3's "Large" estimate.

A leftover, unused `isOverloaded` predicate and `PlatformSignatureResolver.isOverloadedInBindings()` helper already exist in the codebase (`PythonGeneratorPredicates.kt`) but are wired into zero templates — they read like an abandoned first attempt at exactly this fix and are the natural starting point for D0 rather than new machinery.

Section 3 below is a full audit table of every `feature(...)` line against this plan's phase assignments, so the rest of the plan can be trusted at a glance.

---

## 1. Overview

Phase 8 narrowed ~40 functional features out of the `python` generator list to achieve a clean compile. Phase A (A1-A7) and Phase C (C1-C4) are complete and verified against generated output. Phase B (B1-B6) is complete per its own status notes (not re-audited in this revision). Phase D is **enabled but broken**, and its root cause has been re-diagnosed (§2.4, §0). Phases E-K have not been re-audited against the current codebase in this revision; treat their status as inherited from v1 until each is opened.

### 1.1 Root-Cause Categories (updated)

| Gap ID  | Description                                                                                                                                | Status (2026-07-20)                                                                                          | Affected Features |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **G1**  | Constructor/argument-count template bugs                                                                                                    | ✅ Resolved (Phase A/B)                                                                                          | BuiltinTypes, Strings, Enums, Structs, Classes, Interfaces, TypeDefs, InstanceInStruct, StructsInTypes, StructsImmutable, StructsWithCompanion, FieldConstructors, Nesting |
| **G2**  | Property binding                                                                                                                             | ✅ Resolved (Phase C)                                                                                            | Properties, NoCache, CppConst, CppNoexcept                                                                                                                                 |
| **G3**  | Inheritance trampoline — inherited pure-virtual methods not overridden                                                                       | ✅ **Resolved.** `Pybind11Class.mustache` / `Pybind11Interface.mustache` both already loop `{{#inheritedFunctions}}` in the trampoline section. No longer a blocker for D1/D2. | Inheritance, MultipleInheritance, MethodOverloading, RefEquality, Visibility                                                                                               |
| **G4**  | Method overloading — Python does not support overloaded method names                                                                        | 🟡 **Partially resolved.** pybind11-native side (`overload_cast`) is done. `.py` wrapper layer uses `*args`/`**kwargs` dispatcher (D0 steps 1-3, done in prior commits). `.pyi` stub layer now emits `@typing.overload`-decorated signatures (D0 step 4, done). Remaining: D0 step 5 (update `PythonOverloadsValidator` messaging) and D1-D3 verification. See §2.4. | MethodOverloading, Properties, Defaults, **and, newly confirmed, Inheritance, MultipleInheritance, Errors, ExternalTypes**                                                |
| **G5**  | Generic/collection type binding                                                                                                              | Not re-audited                                                                                                   | GenericTypes, Lambdas, Defaults, Locales, RefEquality                                                                                                                      |
| **G6**  | External type binding                                                                                                                        | Not re-audited; `ExternalTypes`/`Errors` already enabled in CMakeLists, unclear how much beyond G4 is blocking them | ExternalTypes, DartExternalTypes, Defaults, Errors                                                                                                                         |
| **G7**  | Error/exception handling                                                                                                                     | Not re-audited                                                                                                   | Errors, Blob                                                                                                                                                               |
| **G8**  | Lambda/callback binding                                                                                                                      | Not re-audited                                                                                                   | Lambdas, ComplexListeners, ListenersWithReturnValues, CallbacksWithThreads                                                                                                 |
| **G9**  | Visibility/internal filtering                                                                                                                | Not re-audited                                                                                                   | Visibility, Comments                                                                                                                                                       |
| **G10** | Naming/package resolution                                                                                                                    | Not re-audited                                                                                                   | UnderscorePackage, CrossPackageNameClash, PlatformNames                                                                                                                    |
| **G11** | Doc comment preservation                                                                                                                     | Not re-audited                                                                                                   | Comments                                                                                                                                                                   |
| **G12** | Threading/GIL                                                                                                                                | Not re-audited                                                                                                   | CallbacksWithThreads                                                                                                                                                       |
| **G13** | Referential equality                                                                                                                         | Not re-audited                                                                                                   | RefEquality, Equatable                                                                                                                                                     |
| **G14** | Locale type                                                                                                                                  | Not re-audited                                                                                                   | Locales                                                                                                                                                                    |

### 1.2 Inter-Feature Dependency Graph

Unchanged from v1 — see [phase8_followup_plan.md §1.2](./phase8_followup_plan.md). The one structural addition: everything in Phase D and the `ExternalTypes`/`Errors` legs of Phase E now share a dependency on the new D0 fix below.

---

## 2. Implementation Phases

### Phase A — Basic Type System (G1) [Complete]

Unchanged from v1. `BuiltinTypes`, `Strings`, `Enums`, `TypeDefs`, `Structs`, `Classes`, `Interfaces` all compile, are enabled for `python` in `functional/CMakeLists.txt`, and their focused tests pass per the A1-A7 status notes in the v1 document.

### Phase B — Structs & Nesting (G1) [Complete]

Unchanged from v1. `StructsImmutable`, `StructsInTypes`, `StructsWithCompanion`, `FieldConstructors`, `InstanceInStruct`, `Nesting` (minus `NestedInheritance.lime`, deferred to Phase K) — see the detailed B4/B5 fix descriptions in v1 for the two real generator bugs found and fixed (`hasDefaultConstructor` predicate, `PythonStruct.mustache` native-object detection in `__init__`).

### Phase C — Properties & Const/Noexcept (G2) [Complete]

Unchanged from v1. `Properties`, `CppConst`, `CppNoexcept`, `NoCache` all verified end-to-end at runtime via the CPython 3.14 interpreter. The interface-property trampoline fix (`PYBIND11_OVERRIDE_PURE` instead of `PYBIND11_OVERRIDE`) done here is almost certainly what carried G3's inherited-function trampoline loop into `Pybind11Class.mustache`/`Pybind11Interface.mustache` as a side effect.

---

### Phase D — Inheritance & Overloading (G3 resolved, G4 in progress) [Enabled, failing]

**Goal (revised)**: G3 no longer needs work. The remaining goal is entirely G4: make the generated **Python wrapper layer** support overloaded names, on top of the pybind11-native layer which already does.

#### D0: Wrapper-Layer Overload Dispatch (G4) — NEW, do this first

**Problem** (verified against generated golden output, not just inferred): `PythonClass.mustache`/`PythonInterface.mustache` loop `{{#functions}}...{{>python/PythonFunction}}{{/functions}}` with no grouping by resolved name, and `PythonFunction.mustache` emits a fixed-signature `def <name>(...)` per Lime function. The generated `smoke/method_overloads` golden `MethodOverloads.py` currently contains **eight** `def is_boolean(...)` definitions in a single class body — only the last (`def is_boolean(self) -> bool`) is reachable; the other seven are dead code that Python silently discards at class-definition time. The identical pattern shows up in the `smoke/inheritance` golden (`InterfaceWithOverloads.py`, `parent_method` defined twice). The `.pyi` stub has the same defect.

**Fix**:

1. **Group functions by resolved Python name** when building the template context for `PythonClass.mustache`/`PythonInterface.mustache` (own + inherited, mirroring what `isCppOverloaded` already does on the pybind11 side). Wire up the existing-but-unused `isOverloaded` predicate / `PlatformSignatureResolver.isOverloadedInBindings()` rather than inventing new plumbing — they already do the grouping logic, they're just not called from anywhere.
2. For each group, emit **one** wrapper method (the first Lime function in declaration order is a fine representative for parameter-name purposes). Change `PythonFunction.mustache`'s body, for grouped methods only, from the current fixed-signature form to a generic pass-through:
   ```python
   def is_boolean(self, *args, **kwargs):
       """..."""
       native_args = [a._native if hasattr(a, "_native") else a for a in args]
       native_kwargs = {k: (v._native if hasattr(v, "_native") else v) for k, v in kwargs.items()}
       result = self._native.is_boolean(*native_args, **native_kwargs)
       ...
   ```
   This is the same wrapper-unwrap pattern already used for the B4/B5 struct fixes (`hasattr(x, "_native")`). The real overload resolution still happens in C++, via the `py::overload_cast` chain that already exists — the wrapper only needs to strip `_native` off wrapper-typed arguments before forwarding.
3. **Return-value wrapping**: for the D3/D1/D2 scope today, every overload group has a single shared return type (`isBoolean` always returns `Boolean`; the `create(...)` factory groups always return the declaring type). Keep today's simple "wrap if `returnType` is a wrapper type" logic keyed off the representative function. Flag mixed-return-type overload groups as an explicit **not handled** case — none exist in the currently-enabled lime files, but a validator warning (see D0 step 5) should catch it if one shows up later (e.g. in Defaults/GenericTypes).
4. **`.pyi` stubs get a different, better fix** ✅ **Done (2026-08-10).** Unlike the runtime `.py`, stub files support real `@typing.overload` stacking, which is strictly more useful to IDE/mypy users than a lossy `*args: Any`. `PythonStubFunction.mustache` now emits `@typing.overload` before each overloaded signature. A new `isPythonOverloaded` predicate (grouping by resolved Python name, same key as `isFirstOverload`) gates the decorator. **No trailing undecorated catch-all** is emitted — `.pyi` files may stack `@overload`-decorated signatures with no implementation following them, since a stub never executes. Adding a synthetic catch-all would itself be an undecorated same-named definition (the exact redefinition problem this fixes) and would misrepresent the public contract. See [method_overload_refactoring_plan.md](./method_overload_refactoring_plan.md) for the full design rationale.
5. **Update `PythonOverloadsValidator`** messaging once this lands — the current text ("Python does not support overloaded methods... is overloaded") becomes actively misleading, since overloading is now supported. Narrow the warning to fire only when pybind11 genuinely can't disambiguate at the C++ level (e.g. two overloads that differ only by `Ref`/`const`), and point users at `@Python(Name=...)` as the escape hatch for those cases. That attribute is already parsed (`PythonNameResolver.getPlatformName`), it's just not exercised by any currently-enabled functional feature.
6. **Constructors ride the same code path — verify, don't re-implement.** Named Lime constructors (e.g. `ConstructorOverloads.create(...)`, a 6-way overload in `MethodOverloads.lime`) flow through the same `functions` collection and the `isStatic` branch in both `Pybind11Function.mustache` and `PythonFunction.mustache`, so steps 1-3 should cover them for free. Add explicit test coverage rather than new template branches.

**Affected files**: `PythonGeneratorPredicates.kt` (wire up grouping), `PythonClass.mustache`, `PythonInterface.mustache`, `PythonFunction.mustache`, `PythonStubClass.mustache`, `PythonStubInterface.mustache`, `PythonStubFunction.mustache`, `PythonOverloadsValidator.kt`.

**Completed subset** (2026-08-10): `PythonGeneratorPredicates.kt` (added `isPythonOverloaded` predicate) and `PythonStubFunction.mustache` (emit `@typing.overload` decorator). Smoke goldens regenerated for all affected fixtures. Functional tests pass (18/18 in `method_overloads_test.py`). See [method_overload_refactoring_plan.md](./method_overload_refactoring_plan.md) for the step-1 implementation report.

**Effort**: Medium (re-estimated down from the "Large" in v1, now that the pybind11-native half is confirmed already done).

#### D1: Inheritance (G3 resolved; blocked only by D0)

`Inheritance` is already `python`-enabled in `functional/CMakeLists.txt`. The trampoline fix v1 described (iterate `inheritedFunctions` in `Pybind11Interface.mustache`/`Pybind11Class.mustache`) is already present. `Inheritance.lime` itself contains one overloaded name (`getData`), so this feature is almost certainly blocked purely by D0 today. After D0 lands: rebuild, force-regenerate (see the gotcha banner at the top), run the inheritance pytest, and confirm. The three sub-files noted in v1 as needing temporary skips (`ConstructorOverride.lime` → Errors, `ListenerInheritanceArrays.lime` → GenericTypes, `InterfaceWithLambda.lime` → Lambdas) should still be skipped for now — those are genuine unmet cross-phase dependencies, unrelated to D0.

**Deps**: D0. **Effort**: Small (verification only, assuming D0 is the sole remaining blocker — confirm before closing).

#### D2: MultipleInheritance (G3 resolved; blocked only by D0)

Same situation as D1: already `python`-enabled, `MultipleInheritance.lime` has two overloaded names (`parentFunction`, `childFunction`), no other known blocker.

**Deps**: D0, D1. **Effort**: Small (verification only).

#### D3: MethodOverloading (G4, now mostly a D0 consumer)

`MethodOverloads.lime` and `InheritanceOverloads.lime` are already `python`-enabled. Once D0 lands, this becomes a verification + test-coverage task rather than new generator work:

- Rebuild, force-regenerate, confirm the golden `MethodOverloads.py`/`.pyi` now have one dispatching `is_boolean`/`is_float` method each (or `@overload`-stacked in the `.pyi`).
- `functional-tests/functional/python/test/method_overloads_test.py` exists and covers all 9 `isBoolean` overloads, all 6 `ConstructorOverloads.create` overloads, and all 3 `StructConstructorOverloads.create` overloads (18 tests total, all passing as of 2026-08-10). `InheritanceOverloads.lime` coverage is still TODO.
- Regenerate and inspect the golden smoke fixtures that also exercise overloading and will change shape under D0: `smoke/method_overloads` (multiple files), `smoke/inheritance` (`InterfaceWithOverloads`), `smoke/external_types` (`ClassWithOverloads`, `StructWithOverloads`), `smoke/durations` (`DurationOverloads`), `smoke/lambdas` (`OverloadedLambda`, not in scope for python yet but will regenerate if touched).

**Deps**: D0. **Effort**: Small-Medium (mostly test-writing + golden regeneration, not template work).

**Exit criteria for Phase D**: D0 lands; D1/D2/D3 pytest suites pass with the three `Inheritance` sub-files still skipped per v1's Phase D note.

---

### Phase E — External Types & Error Handling (G6, G7) [Partially enabled, not re-audited]

`ExternalTypes` and `Errors` are already `python`-enabled in `functional/CMakeLists.txt`, contrary to v1's framing of Phase E as blocked behind Phase D completion. Both lime inputs contain overloaded names (`ExternalTypes.lime`: `allOverloadsExposed` ×3, `some_Method` ×2; `Errors.lime`: `methodWithError` ×2), so **both are likely blocked at least partly by the same D0 gap**. Recommendation: after D0 lands, rebuild these two features before assuming any remaining failure is G6/G7-specific — it may turn out most of Phase E's originally-scoped work is already done and all that's left is the overload fix plus test coverage, similar to Phase D. `DartExternalTypes` (E2) is **not** currently `python`-enabled in CMakeLists (only `dart`) — confirm whether that's intentional (Dart-only external-type pattern) before carrying it forward as a Python phase item.

Everything else in this phase (E1's external-name/include resolution, E3's exception-translation wiring for non-overload cases, E4/`Blob`) is unchanged from v1 pending a dedicated audit.

---

### Phase F — Generic/Collection Types (G5) [Not re-audited]

Unchanged from v1. `GenericTypes` and `Defaults` are not `python`-enabled in the current `functional/CMakeLists.txt`, consistent with v1.

### Phase G — Lambdas/Callbacks (G8) [Not re-audited]

Unchanged from v1. `Lambdas` is not `python`-enabled, consistent with v1.

### Phase H — Naming, Visibility & Docs (G9, G10, G11) [Not re-audited]

Unchanged from v1, with one correction: `PlatformNames` is confirmed not `python`-enabled in the current CMakeLists, consistent with v1's H1 placement — but note the underlying `@Python(Name=...)` attribute-resolution mechanism this phase would exercise is already implemented (`PythonNameResolver.getPlatformName`) and is being recommended as D0's fallback path for genuinely ambiguous overloads. H1 itself (the dedicated `PlatformNames.lime` functional feature) can stay where it is in the sequence; it isn't a dependency of D0.

### Phase I — Equality & Locale (G13, G14) [Not re-audited]

Unchanged from v1.

### Phase J — Listeners & Threading (G8, G12) [Not re-audited]

Unchanged from v1. Note `Listeners` (the base feature, distinct from `ComplexListeners`/`ListenersWithReturnValues`) isn't `python`-enabled and also isn't listed anywhere in v1's phase tables — it's untracked by this plan either way; fold it into Phase J scoping when that phase is opened.

### Phase K — Cleanup & Revisit Skipped Sub-files [Depends on all above]

Unchanged from v1, plus: once D0/D1/D2/D3 close out, re-check whether `ConstructorOverride.lime` (K1) is still blocked on `Errors` (E3) given E3's status is now uncertain pending its own re-audit.

---

## 3. CMakeLists Enablement Audit (2026-07-20)

Every `feature(...)` line in `functional/CMakeLists.txt`, cross-referenced against this plan. "Phase" is this plan's assignment; "Consistent?" flags mismatches between what's enabled and what the plan expected.

| Feature | `python` enabled? | Plan phase | Consistent with plan? |
| --- | --- | --- | --- |
| Strings | ✅ | A2 | ✅ |
| BuiltinTypes | ✅ | A1 | ✅ |
| Classes | ✅ | A6 | ✅ |
| Interfaces | ✅ | A7 | ✅ |
| Structs | ✅ | A5 | ✅ |
| TypeDefs | ✅ | A4 | ✅ |
| Enums | ✅ | A3 | ✅ |
| StructsInTypes | ✅ | B2 | ✅ |
| StructsImmutable | ✅ | B1 | ✅ |
| FieldConstructors | ✅ | B4 | ✅ |
| InstanceInStruct | ✅ | B5 | ✅ |
| StructsWithCompanion | ✅ | B3 | ✅ |
| Nesting | ✅ | B6 | ✅ |
| Properties | ✅ | C1 | ✅ |
| CppConst | ✅ | C2 | ✅ |
| CppNoexcept | ✅ | C3 | ✅ |
| NoCache | ✅ | C4 | ✅ |
| **Inheritance** | ✅ | D1 | ❌ v1 called this blocked; already enabled, root cause re-diagnosed (§2, D1) |
| **MultipleInheritance** | ✅ | D2 | ❌ same as above |
| **MethodOverloading** | ✅ | D3 | ❌ same as above — this was the original prompt for this audit |
| **ExternalTypes** | ✅ | E1 | ❌ v1 called this blocked behind D1; already enabled |
| **Errors** | ✅ | E3 | ❌ v1 called this blocked behind E1; already enabled |
| DartExternalTypes | ❌ (dart only) | E2 | ⚠️ v1 lists this as a python phase item; not currently python-targeted at all — confirm scope |
| Blob | ❌ | E4 | ✅ |
| GenericTypes | ❌ | F1 | ✅ |
| Defaults | ❌ | F2 | ✅ |
| Lambdas | ❌ | G1 | ✅ |
| PlatformNames | ❌ | H1 | ✅ |
| Visibility | ❌ | H2 | ✅ |
| UnderscorePackage | ❌ | H3 | ✅ |
| CrossPackageNameClash | ❌ | H4 | ✅ |
| Comments | ❌ | H5 | ✅ |
| Equatable | ❌ | I1 | ✅ |
| Locales | ❌ | I2 | ✅ |
| Listeners | ❌ | untracked | — not in v1's tables either |
| ComplexListeners | ❌ | J1 | ✅ |
| ListenersWithReturnValues | ❌ | J2 | ✅ |
| CallbacksWithThreads | ❌ (no swift either) | J3 | ✅ |
| Nullable | ❌ | untracked (referenced only via a stale-import note in v1) | — |
| SkipAttribute | ❌ | untracked | — likely belongs near H2/Visibility |
| **CircularDependencies** | ✅ | *none* | ⚠️ enabled, not tracked by this plan at all — see §7.1 |
| **Constants** | ✅ | *none (referenced only as a B3 dependency, "✅")* | ⚠️ enabled, appears already done, not tracked |
| **Dates** | ✅ | *none (v1: "already enabled")* | ✅ (matches v1's framing) |
| **Durations** | ✅ | *none (v1: "already enabled")* | ✅ (matches v1's framing) |
| **DeclarationOrder** | ✅ | *none* | ⚠️ enabled, not tracked — see §7.1 |
| **EscapedNames** | ✅ | *none* | ⚠️ enabled, not tracked — see §7.1 |
| **FullName** | ✅ (dart+python only) | *none* | ⚠️ enabled, not tracked — see §7.1 |

---

## 4. Effort Estimates (revised)

| Phase     | Features | Estimated Effort | Key Risk                                            |
| --------- | -------- | ----------------- | --------------------------------------------------- |
| A         | 7        | Done               | —                                                     |
| B         | 6        | Done               | —                                                     |
| C         | 4        | Done               | —                                                     |
| **D0**    | 1 (cross-cutting) | **1-2 days** (step 4 done; steps 1-3 done in prior commits) | Medium — return-type-wrapping edge cases if a future feature introduces mixed-return-type overload groups |
| D1-D3     | 3        | **1-2 days**       | Low, now that D0 carries the hard part — mostly verification + test-writing |
| E1, E3    | 2        | **2-4 days** (re-audit needed) | Medium — unclear how much of the original G6/G7 scope is still outstanding once D0 unblocks generation |
| E2, E4    | 2        | 3-4 days (unchanged from v1) | Medium |
| F         | 2        | 3-4 days (unchanged) | Medium |
| G         | 1        | 3-4 days (unchanged) | Medium |
| H         | 5        | 2-3 days (unchanged) | Low |
| I         | 2        | 2-3 days (unchanged) | Medium |
| J         | 3        | 4-5 days (unchanged) | High |
| K         | 5 tasks + untracked-feature cleanup (§7.1) | 1-2 days (unchanged) + 0.5 day for §7.1 | Low |

Net effect of this revision: total effort drops somewhat, because the hardest part of Phase D (G3 trampoline work) turned out to already be done, and G4's fix is now understood to be a single cross-cutting template change rather than per-feature "Large" work repeated three times.

---

## 5. Key Design Decisions

### 5.1 Overload Resolution (G4) — updated

v1 posed this as a choice between `py::overload_cast` and `@Python(Name=...)` renaming. In practice **both are needed, at different layers, and the choice is no longer open**:

- **pybind11-native layer**: `py::overload_cast` — already implemented in `Pybind11Function.mustache`, no further work.
- **Python wrapper layer**: generic `*args`/`**kwargs` pass-through that delegates to the native overload set (D0). This is not optional — it's the only way to get more than one overload reachable through the wrapper class at all, since Python class bodies can't hold two same-named methods the way C++ classes can.
- **`@Python(Name=...)` rename**: kept as the fallback for the narrow case where pybind11 itself can't disambiguate two C++ overloads (e.g. differing only by `Ref`), which the generic wrapper can't paper over either. Not needed for any currently-enabled feature.

### 5.2 External Type Binding (G6)

Unchanged from v1 — recommend Option 2 (skip binding, use the C++ type directly). Not re-audited against current code in this revision.

### 5.3 Threading/GIL (G12)

Unchanged from v1.

### 5.4 Locale Type (G14)

Unchanged from v1.

---

## 6. Testing Strategy

Unchanged from v1's steps 1-6, with one addition specific to D0: because the fix changes the **shape** of generated wrapper methods (fixed-signature → `*args`/`**kwargs`) for every overloaded name across every currently-enabled feature, expect golden-file diffs in `smoke/method_overloads`, `smoke/inheritance`, `smoke/external_types`, and `smoke/durations` simultaneously. Regenerate all of them together in one pass (`DUMP_ACTUAL_DIR=... ./gradlew :gluecodium:test --tests "*method_overloads*" --tests "*inheritance*" --tests "*external_types*" --tests "*durations*"` or equivalent) rather than one feature at a time, so the diffs can be reviewed as one coherent change instead of four unrelated-looking ones.

---

## 7. Appendix: Feature-to-Gap Mapping

Unchanged from v1 for phases E2/F-J; D-phase rows updated:

| Feature                   | Gaps        | Phase | Notes                                                                                  |
| -------------------------- | ----------- | ----- | --------------------------------------------------------------------------------------- |
| Inheritance                | G4 (G3 done)| D1    | Trampoline fix already landed; blocked on D0 only, plus 3 known sub-file skips          |
| MultipleInheritance        | G4 (G3 done)| D2    | Same as above                                                                            |
| MethodOverloading          | G4          | D0, D3| Root cause is the wrapper layer, not the pybind11 layer                                 |
| ExternalTypes              | G4 + G6     | D0, E1| Re-audit G6 scope after D0 lands                                                        |
| Errors                     | G4 + G7     | D0, E3| Re-audit G7 scope after D0 lands                                                        |

*(All other rows unchanged from [phase8_followup_plan.md §7](./phase8_followup_plan.md).)*

### 7.1 Untracked features already enabled for `python`

Four features are `python`-enabled in `functional/CMakeLists.txt` but appear in none of this plan's (or v1's) phase tables: `CircularDependencies`, `DeclarationOrder`, `EscapedNames`, `FullName` (plus `Constants`, which v1 references only in passing as an already-satisfied B3 dependency). None of their `.lime` inputs exercise overloading, external types, or any other known gap at a glance (`Circular.lime` is two classes referencing each other with single-signature methods; the others are naming/ordering edge cases). Best guess: these were never part of the original ~40 features narrowed out in Phase 8, and have been passing all along.

**Action for Phase K**: before declaring the functional suite fully green, explicitly run these five and confirm — don't assume "not in the plan" means "already verified." If any fail, they'll need their own phase entry; if they pass, add a one-line confirmation to this document so future revisions don't have to rediscover them.
