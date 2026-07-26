# Phase H Work Plan: Naming, Visibility & Docs (Python Generator)

> **Date**: 2026-07-24
> **Branch**: `python_bind`
> **Status**: Not started — scoping document
> **Related**: [phase8_followup_plan.md](./phase8_followup_plan.md), [phase8_followup_plan_v2.md](./phase8_followup_plan_v2.md), [phase8_status.md](./phase8_status.md)
> **Supersedes**: The `Phase H` section (§2, "Phase H — Naming, Visibility & Docs") in `phase8_followup_plan.md`, expanded into a standalone, actionable plan with a fresh code audit (2026-07-24).

> **⚠️ Gotcha — stale generated code after a generator change (carried over from v1/v2, still applies):** the CMake custom command that invokes Gradle for code generation depends only on the LimeIDL inputs and the options file, not on the published Gluecodium jar. If you edit a template or generator Kotlin source, re-publish, and rebuild **without touching a `.lime` input**, generation is skipped and you will silently test stale output. Always touch a relevant `.lime` file or `rm -rf functional-tests/build-python/functional/gluecodium` before rebuilding, and verify the regenerated file actually changed before concluding a fix failed or succeeded.

---

## 0. Audit summary (2026-07-24)

A fresh pass over `python_bind` HEAD confirms the following for the five Phase H features. None of them are enabled for `python` in `functional-tests/functional/CMakeLists.txt` today, and none of the corresponding `.lime` files carry a `@Skip(Python)` — they are simply not yet in the target list.

| Feature | `python` enabled? | Underlying generator gap status |
|---|---|---|
| `PlatformNames` | ❌ | `@Python(Name=...)` resolution **already implemented** (`PythonNameResolver.getPlatformName`, `PythonNameRules.getPlatformName`/`getPropertyName`). Feature itself just needs enabling + verification. |
| `Visibility` (`VisibilityAttribute.lime` et al.) | ❌ | `isInternal`/`isPublic`/`isNestedInternal` predicates exist in `PythonGeneratorPredicates.kt` but are **not wired into any Python-facing template** — internal functions/properties/fields/constructors currently leak into the generated Python wrapper and pybind11 binding unchanged. This is a real, unimplemented gap (see §2.2). |
| `UnderscorePackage` | ❌ | No package-name-specific logic exists or is needed beyond the generic file-based module resolution (`PythonNameResolver.resolveFileReferenceName`); likely low-risk, verification-only. |
| `CrossPackageNameClash` | ❌ | Same as above — Python modules are already namespaced by package path (`limeElement.path.head`), so same-named types in different packages should resolve to distinct dotted module paths already. Verification-only, but not yet exercised. |
| `Comments` (`Comments.lime`, `CommentsInterface.lime`) | ❌ | Doc-comment plumbing is **partially implemented**: `PythonCommentsProcessor` exists and produces reST/Sphinx-style docstrings, and `PythonClass.mustache`/`PythonInterface.mustache`/`PythonFunction.mustache` already emit `"""{{resolveName comment}}"""` for class- and function-level comments. **Not yet wired**: `PythonStruct.mustache`, `PythonProperty.mustache`, `PythonField.mustache`, `PythonEnumeration.mustache`, and all `PythonStub*.mustache` (`.pyi`) templates have no docstring emission at all. The `hasAnyComment` predicate is defined but unused everywhere. |

**Net assessment**: Phase H is more scoped than the original plan suggested — G10 (naming) is largely done or low-risk, but G9 (visibility) and G11 (doc comments) both have concrete, identified template gaps that need real generator work before the features can be enabled.

---

## 1. Root-cause gaps recap

| Gap ID | Description | Phase H features affected |
|---|---|---|
| **G9** | `@Internal` elements are not filtered out of Python wrapper/pybind11 output | `Visibility` |
| **G10** | Package/name resolution: `@Python(Name=...)`, underscore packages, cross-package clashes | `PlatformNames`, `UnderscorePackage`, `CrossPackageNameClash` |
| **G11** | Doc comment (`//`) propagation to Python docstrings, for all element kinds and `.pyi` stubs | `Comments` |

---

## 2. Work items

### H1 — `PlatformNames` (G10) — verification + small fixes

**Lime file**: `PlatformNames.lime` — a struct, nested struct, nested enum, nested typealias, a class (static method, named constructor, property with distinct getter/setter names), and an interface, each carrying `@Python(Name=...)`-style per-language name overrides today for `Cpp`/`Java`/`Kotlin`/`Swift`/`Dart` but **no `@Python(...)` annotations yet**.

**Findings**:
- `PythonNameResolver.getPlatformName` / `PythonNameRules.getPlatformName` / `getPropertyName` already read `limeElement.attributes.get(PYTHON, NAME)` and take priority over the default name-rule-derived name. This is exercised today only by the D0 overload-fallback recommendation in `phase8_followup_plan_v2.md`, never by a real functional feature.
- No generator code changes are anticipated for the core name-substitution mechanism.

**Tasks**:
1. Add `@Python("...")` annotations to `PlatformNames.lime` mirroring the existing `@Cpp`/`@Java`/`@Kotlin`/`@Swift`/`@Dart` annotations (struct, nested struct, nested enum + enumerator, nested typealias, class, static method + its parameter, named constructor + its parameter, property with distinct getter/setter names, listener interface + method + parameter).
2. Enable `python` in the `feature(PlatformNames ...)` line in `functional-tests/functional/CMakeLists.txt`.
3. Force-regenerate, rebuild via `functional-tests/scripts/build-python-functional --publish`, and confirm the generated `PlatformNames.py`/`.pyi` and pybind11 binding use the Python-specific names end to end (module attribute names, wrapper method/property names, parameter names in generated docstrings/signatures).
4. Write `functional-tests/functional/python/test/platform_names_test.py` (mirroring the Swift/Kotlin/Dart equivalents) asserting the renamed struct/enum/class/interface members are reachable under their `@Python(Name=...)` names.
5. Regenerate and inspect smoke goldens under `gluecodium/src/test/resources/smoke/platform_names/` for the new Python output.

**Deps**: None (builds on completed Phase A/C). **Effort**: Small.

---

### H2 — `Visibility` (G9) — real generator work

**Lime files**: `VisibilityAttribute.lime`, `VisibilityInternal.lime`, `VisibilityPlatform.lime`, `VisibilityPlatformReverse.lime`, `InternalFields.lime`.

**Problem** (confirmed by code audit): `PythonGeneratorPredicates.kt` defines `isInternal`, `isPublic`, and `isNestedInternal`, and `PythonGenerator.kt` uses `isPublic` only to filter **includes** for the pybind11 header (`pybind11IncludeCollector`). No Python-facing template (`PythonClass.mustache`, `PythonInterface.mustache`, `PythonStruct.mustache`, `PythonFunction.mustache`, `PythonProperty.mustache`, `PythonField.mustache`, nor any `PythonStub*.mustache`) checks `isInternal`/`isPublic` before emitting a function, property, field, constructor, or nested type. Nor do the `Pybind11*.mustache` templates skip internal members when generating the C++ binding. As a result, today, `@Internal` elements would be emitted into both the pybind11 binding and the Python wrapper exactly like public ones — the opposite of Java/Kotlin/Swift/Dart, which all suppress or specially mark internal members.

**Reference behavior** (from other generators, to mirror):
- Java: `JavaVisibilityResolver` — `isInternal(element)` returns empty visibility modifier (i.e. package-private) instead of `public`.
- Kotlin/Swift/Dart: dedicated `*VisibilityResolver` classes; Kotlin additionally has `KotlinInterfacesValidator` rejecting `@Internal` on interface members it cannot represent (interfaces can't have non-public members in some languages).
- **Python decision needed**: Python has no formal access-control keyword. Two options, consistent with the "internal" contract used elsewhere in Gluecodium (internal = library-internal API, not meant for external consumers, but callable from other internal Gluecodium-generated code / same package):
  1. **Suppress generation entirely** for `@Internal` functions/properties/fields/constructors/nested types in the *public* Python wrapper (mirrors Java's "package-private is invisible outside the package" intent, since Python has no package-private equivalent) — but the pybind11-native layer likely still needs to expose them so that other internal Python code (or the C++ core) can use them internally.
  2. **Emit with a single leading underscore** (`_fooBar`), Python's conventional "internal, not part of the public API" marker, matching PEP 8. This keeps the API reachable (as internal features may be relied upon by other generated code or same-package callers) while clearly signaling non-public intent.
  - **Recommendation**: adopt option 2 (leading-underscore convention) for consistency with idiomatic Python and to avoid silently dropping functionality that `SomeStructWithInternalMembers` (which mixes public and internal members in the same struct) requires to remain internally consistent. This mirrors the approach already used for name mangling in other Python-ecosystem bindings (e.g. `_native`).
  - Cross-check this decision against how `Internal` is documented in `docs/lime_attributes.md` before implementing, since the semantic contract (visible only within the same package vs. hidden entirely) affects whether nested full suppression is instead correct for some cases (e.g. `@Internal` on an entire class/interface, vs. `@Internal` on one member of an otherwise-public struct).

**Sub-cases to handle** (all present in `VisibilityAttribute.lime`):
1. `@Internal class InternalAttributeClassWithFunctions` — whole class marked internal, including two overloaded constructors.
2. `@Internal internalField: String` inside an otherwise-public struct (`PublicStructWithNonDefaultInternalAttributeField`) — struct itself stays public, one field is internal; struct's field-based constructors need to still work correctly around the internal field's position/defaultedness.
3. `@Internal static property fooBar: String` — internal static property.
4. `@Kotlin(Skip) @Java(Skip=...) interface WithInternalAttributeProperty { @Internal property foo }` — internal property on an interface; per the existing Kotlin comment, "Kotlin language does not allow internal elements in interfaces" — confirm whether Python (pybind11 property binding) has an equivalent constraint or can support it.
5. `@Internal interface InternalAttributeInterfaceParent` — whole interface internal (used as a parent by a public child in `VisibilityInternal.lime`/`VisibilityPlatform.lime` — needs D-phase inheritance support already in place).
6. `@Internal lambda SomeInternalLambda` — internal lambda type alias (blocked on Phase G, `Lambdas`, for full lambda binding — may need to be temporarily skipped/deferred if Lambdas isn't done first).
7. `@Internal narrow interface SomeInternalInterface` — internal narrow interface.
8. `@Internal struct SomeInternalStructWithMembers` — whole struct internal, including its own static factory.
9. `SomeStructWithInternalMembers` — public struct with per-member `@Internal` on functions, fields (including ones referencing the internal lambda/narrow interface above — again gated on Phase G), a named constructor, a plain function, `@Skip(Swift, Dart) @Internal(Java, Kotlin)` (platform-conditional internal — confirm current PYTHON attribute parsing correctly treats `@Internal(Java, Kotlin)` as *not* internal for Python), and a static function.
10. `SomeStructWithInternalFreeArgsCtor` / `SomeStructWithInternalAllArgsCtor` / `SomeStructWithInternalFieldConstructor` — internal fields interacting with the B4 field-constructor logic (`hasDefaultConstructor`/`needsAllFieldsConstructor`/`hasPartialDefaults` predicates in `PythonGeneratorPredicates.kt`) — verify internal fields don't corrupt constructor-arity predicates that were fixed in Phase B.
11. `SomeInternalClassWithMembers.SomeNestedInternalClass` — nested internal class inside an internal class (interacts with the B6 nested-type flattening logic).

**Tasks**:
1. Confirm the semantic decision (leading-underscore vs. suppression) with a design note, referencing `docs/lime_attributes.md`'s definition of `@Internal`.
2. Wire `isInternal`/`isNestedInternal` into:
   - `PythonClass.mustache`, `PythonInterface.mustache`, `PythonStruct.mustache` — per-function/property/field/constructor/nested-enum gating (skip or underscore-prefix, per the design decision).
   - `PythonFunction.mustache`, `PythonProperty.mustache`, `PythonField.mustache`, `PythonConstant.mustache` — name resolution changes if the underscore convention is chosen (likely centralized in `PythonNameResolver`/`PythonNameRules` behind a new "isInternal → prefix `_`" rule, rather than per-template string concatenation).
   - All `PythonStub*.mustache` — the `.pyi` stubs must mirror whatever the `.py` output does.
   - `Pybind11Class.mustache`, `Pybind11Interface.mustache`, `Pybind11Struct.mustache` — decide whether pybind11 bindings expose internal members under a mangled/underscore C++-side attribute name too, or keep the native binding fully exposed and only rename in the Python wrapper. (Likely keep pybind11-native attribute names unchanged since they're never seen by end users, and rename only in the wrapper.)
3. Add or extend `PythonGeneratorPredicates.kt` if a combined "isInternal, accounting for nested-parent internal-ness" predicate is needed at each of function/property/field/constructor level (reuse `isNestedInternal` where a whole enclosing container is internal).
4. Verify the per-platform conditional form `@Skip(Swift, Dart) @Internal(Java, Kotlin)` — confirm `CommonGeneratorPredicates.isInternal(element, PYTHON)` correctly returns `false` for Python here (it should, since the attribute is scoped to `Java, Kotlin` only) — add a regression test/assertion for this specific case since it's easy to get backwards.
5. Enable `python` for `Visibility` in `functional-tests/functional/CMakeLists.txt`. Confirm whether `SomeInternalLambda`/`SomeInternalInterface`-dependent members need temporary exclusion pending Phase G (Lambdas) — if so, document precisely which sub-file/class needs a temporary skip, following the pattern used for `Inheritance`'s `ConstructorOverride.lime`/`ListenerInheritanceArrays.lime`/`InterfaceWithLambda.lime` skips in Phase D.
6. Write `functional-tests/functional/python/test/visibility_test.py` covering each sub-case above; assert internal members are reachable (if underscore convention) or truly absent (if suppression) as designed.
7. Regenerate smoke goldens under `gluecodium/src/test/resources/smoke/visibility_attribute/` (and `internal_fields/` for `InternalFields.lime`, if in scope) for the new Python output; review the diff carefully since this changes many generated files at once.

**Deps**: D1 (Inheritance, for `@Internal interface` used as a parent), possibly G1 (Lambdas, for the two lambda/narrow-interface-typed internal members — confirm whether these can be stubbed/skipped instead of fully blocking H2). **Effort**: Medium-Large (real design decision + multi-template change + broad golden-file impact).

---

### H3 — `UnderscorePackage` (G10) — verification only

**Lime files**: `UnderscorePackage.lime` (package `test_off` or similar underscore-containing package name), `UseUnderscorePackage.lime` (cross-package consumer).

**Findings**: Python module paths are derived from `limeElement.path.head` (the LIME package path) joined with `.`, via `PythonNameResolver.resolveFileReferenceName`/`createImport` in `PythonImportResolver`. An underscore in a package segment is already a syntactically valid Python module/package name component (unlike, say, Java, which needs no special handling either) — there is no known reason this wouldn't already work correctly, but it has never been exercised end-to-end for Python.

**Tasks**:
1. Enable `python` in the `feature(UnderscorePackage ...)` line in `functional-tests/functional/CMakeLists.txt`.
2. Force-regenerate, rebuild, and inspect the generated package directory structure (`__init__.py` placement per `PythonGenerator.generateCommonFiles`'s `packageInitFiles` logic) to confirm the underscore-named package directory is created correctly and importable.
3. Write `functional-tests/functional/python/test/underscore_package_test.py` importing across the two packages and asserting no name-mangling artifacts.
4. Regenerate smoke goldens under `gluecodium/src/test/resources/smoke/name_rules/` or wherever `UnderscorePackage` goldens live; confirm no diffs beyond enabling Python output.

**Deps**: None. **Effort**: Small (verification-only, low risk of failure).

---

### H4 — `CrossPackageNameClash` (G10) — verification only

**Lime files**: `CrossPackageNameClashA.lime`, `CrossPackageNameClashB.lime`, `CrossPackageNameClashC.lime` — each declaring a same-named type (`Alphabet`) in a different package (`test`, `test.foo`, `test.bar`).

**Findings**: Because Python modules are namespaced by the full package path (`test.Alphabet`, `test.foo.Alphabet`, `test.bar.Alphabet`), and `PythonGenerator.getPythonTypes`'s duplicate-filename exclusion (`nameRules.getPythonFileName(it) !in duplicateFileNames`) already exists to avoid two *same-named nested types in the same package* colliding on a single `.py` filename — a distinct risk from cross-package name clashes, which are resolved by directory nesting instead. No known blocker, but the `resolveRegisterName` mechanism (used for the pybind11 C++ `register_*` function name, already includes the package path specifically "so that two types with the same short name in different packages... do not collide at link time") suggests this exact scenario was anticipated and partially built for, but the collector/register-order logic (`topologicalSort` in `generateCommonFiles`) has not been validated against three same-named types simultaneously.

**Tasks**:
1. Enable `python` in the `feature(CrossPackageNameClash ...)` line in `functional-tests/functional/CMakeLists.txt`.
2. Force-regenerate; confirm the three `Alphabet` types are placed at `test/Alphabet.py`, `test/foo/Alphabet.py`, `test/bar/Alphabet.py` and the pybind11 `register_*` function names (`resolveRegisterName`) do not collide (`test_Alphabet`, `test_foo_Alphabet`, `test_bar_Alphabet`).
3. Confirm imports in any cross-referencing type correctly disambiguate via full dotted path (not just bare `Alphabet`).
4. Write `functional-tests/functional/python/test/cross_package_name_clash_test.py` importing all three and asserting they are distinct classes.
5. Regenerate smoke goldens.

**Deps**: None. **Effort**: Small.

---

### H5 — `Comments` (G11) — doc comment propagation for all element kinds + stubs

**Lime files**: `Comments.lime`, `CommentsInterface.lime`.

**Findings** (confirmed by code/template audit):
- `PythonCommentsProcessor` (extends the shared `CommentsProcessor`) is fully implemented: it produces reST/Sphinx-flavored text, escapes embedded double quotes so they don't break a `"""..."""` docstring, remaps Markdown links to `` `ref` `` inline-code style, and unwraps autolinks. `PythonNameResolver.resolveComment` wires it up and is reachable via `resolveName(comment)` in templates.
- **Already emitting docstrings**: `PythonClass.mustache` and `PythonInterface.mustache` (class-level `"""{{resolveName comment}}"""` right after the `class` line) and `PythonFunction.mustache` (method-level `"""{{resolveName comment}}"""`, only in the non-stub, non-overloaded-and-not-first-overload branches — need to confirm this is present in *all* branches, including the static/instance/overloaded branches, not just some).
- **Missing entirely** (verified no `{{comment}}` / `{{resolveName comment}}` usage in these templates):
  - `PythonStruct.mustache` — no struct-level or field-level docstring.
  - `PythonProperty.mustache` — no property docstring (Python properties support docstrings via the getter function's `__doc__`).
  - `PythonField.mustache` — struct fields have no natural place for a per-field docstring in a dataclass-less plain class, needs a design decision (e.g. inline `#:` Sphinx-style comment above the field, or omit).
  - `PythonEnumeration.mustache` — no enum-level or enumerator-level docstring (Python's `enum.Enum` supports assigning `__doc__` and, less standard, per-member help text).
  - `PythonConstant.mustache` — module-level constants have no attached comment mechanism today.
  - **All `PythonStub*.mustache` files** (`PythonStubClass`, `PythonStubInterface`, `PythonStubStruct`, `PythonStubFunction`, `PythonStubProperty`, `PythonStubField`, `PythonStubEnumeration`, `PythonStubException`, `PythonStubTypeAlias`, `PythonStubLambda`) — none emit any docstring or comment, meaning `.pyi` consumers (IDEs, mypy) get zero doc-comment value even where the runtime `.py` module does have one.
- `hasAnyComment` predicate (`CommonGeneratorPredicates.hasAnyComment(limeElement, "Python")`) is defined in `PythonGeneratorPredicates.kt` but never referenced by any template — likely intended to gate whether to emit a docstring block at all (avoiding an empty `""" """`), mirroring how other generators use their own `hasAnyComment` equivalents.

**Tasks**:
1. Audit `PythonFunction.mustache` line-by-line to confirm every code path that emits a `def` also emits `{{#if comment}}"""{{resolveName comment}}"""{{/if}}` — the file is dense/minified Trimou markup with many nested `{{#ifPredicate}}` branches (overloaded/first-overload/static/instance/interface/trampoline combinations); at least one combination may be missing the docstring line. Use `hasAnyComment` (wire it in) instead of the current ad hoc `{{#if comment}}` to match the convention used elsewhere (e.g. Swift/Kotlin) and avoid emitting `""" """` for elements with no doc comment.
2. Add docstring emission to `PythonStruct.mustache` (struct-level, mirroring `PythonClass`) and decide + implement a per-field doc-comment convention for `PythonField.mustache` (recommend Sphinx-style `#:` comment immediately above the field name, since Python has no first-class per-field docstring syntax for plain classes).
3. Add docstring emission to `PythonProperty.mustache` (attach to the getter function body, since a Python `property`'s `__doc__` is sourced from the getter's docstring by default).
4. Add docstring/comment emission to `PythonEnumeration.mustache` for both the enum class and, where feasible, individual enumerators (Python enum members don't support per-member docstrings natively; consider a `#:` comment above each member as the pragmatic option, consistent with Sphinx `autodoc`/`autoenum` conventions).
5. Add a `#:` comment (or equivalent) to `PythonConstant.mustache` for module-level constants.
6. Extend every `PythonStub*.mustache` template to emit the same docstring/comment content as its non-stub counterpart, so `.pyi` consumers get identical documentation.
7. Wire `hasAnyComment` into all of the above instead of ad hoc null/blank checks, for consistency.
8. Enable `python` in the `feature(Comments ...)` line in `functional-tests/functional/CMakeLists.txt`.
9. Force-regenerate, rebuild, and manually inspect generated `Comments.py`/`.pyi` and `CommentsInterface.py`/`.pyi` for correct docstring placement, escaping (verify a comment containing a literal `"` renders safely), and Markdown-to-reST link conversion.
10. Write `functional-tests/functional/python/test/comments_test.py` asserting `__doc__` is non-empty and contains expected substrings for the class, at least one function, one property, one struct field's module source (via `inspect.getsource` or similar), and one enum.
11. Regenerate smoke goldens under `gluecodium/src/test/resources/smoke/comments/`; this is expected to be one of the larger golden-file diffs in Phase H since every currently-enabled Python feature with any doc comment will change once `hasAnyComment`/struct/property/enum docstrings are added — plan to regenerate goldens for *all* currently Python-enabled features in one pass (not just `Comments`) and review as a single coherent diff, per the precedent set in `phase8_followup_plan_v2.md` §6 for the D0 change.

**Deps**: None functionally, but expect broad golden-file churn across all already-enabled Python features (any of them with doc comments in their `.lime` inputs will pick up new struct/property/enum docstrings). **Effort**: Medium (multiple templates, some design decisions for field/enum-member comments, but no new predicates or complex generator logic beyond `hasAnyComment` wiring).

---

## 3. Suggested execution order

```
H3 (UnderscorePackage) ──┐
H4 (CrossPackageNameClash) ├── independent, low-risk, do first/in parallel
H1 (PlatformNames) ───────┘

H5 (Comments) ── independent of H1/H3/H4, but broad golden-file impact;
                 do after H1/H3/H4 land so their goldens are stable first

H2 (Visibility) ── depends on a design decision (§2.2) and, for two
                    lambda/narrow-interface-typed members, on Phase G
                    (Lambdas); do last within Phase H
```

Rationale: H1/H3/H4 are pure verification tasks with essentially no generator code risk — landing them first builds confidence and unblocks their own CMakeLists/CI entries quickly. H5 touches many templates but has a clear, mechanical fix pattern (mirror what already exists for class/function docstrings). H2 is the only item requiring a genuine design decision and has the widest blast radius (every currently-enabled feature with any `@Internal` element, plus new template branches in both the `.py` and `.pyi` and pybind11 layers), so it should land last, once the design decision from §2.2 is confirmed.

---

## 4. Exit criteria for Phase H

- All 5 features (`PlatformNames`, `Visibility`, `UnderscorePackage`, `CrossPackageNameClash`, `Comments`) are enabled for `python` in `functional-tests/functional/CMakeLists.txt`.
- Each feature has a corresponding `functional-tests/functional/python/test/*_test.py` file that passes under the CPython interpreter that built the extension.
- Smoke goldens under `gluecodium/src/test/resources/smoke/` are regenerated and reviewed for `platform_names`, `visibility_attribute` (and `internal_fields` if in scope), `name_rules`/underscore-package location, the cross-package-name-clash location, and `comments`.
- The `@Internal` semantic decision (suppression vs. underscore-prefix) for H2 is documented in this file (or a follow-up note) with rationale, and consistently applied across the `.py`, `.pyi`, and pybind11 layers.
- No regressions in previously-passing Python functional tests (run the full currently-enabled Python pytest suite before and after each Phase H item lands).

## 5. Effort estimate

| Item | Effort | Key risk |
|---|---|---|
| H1 `PlatformNames` | Small | Low |
| H2 `Visibility` | Medium-Large | Design decision + broad template/golden impact; partial dependency on Phase G (Lambdas) for 2 sub-cases |
| H3 `UnderscorePackage` | Small | Low |
| H4 `CrossPackageNameClash` | Small | Low |
| H5 `Comments` | Medium | Broad golden-file churn across all enabled features; per-field/per-enumerator doc convention needs a design call |
| **Total** | **~2-3 days** | Concentrated in H2 and H5 |
