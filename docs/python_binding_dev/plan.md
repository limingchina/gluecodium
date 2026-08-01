# Python Nested-Type Binding Transition Plan

> **Status:** Proposed
> **Scope:** Python wrapper and pybind11 generators
> **Related:** [Python pybind11 design](../python_pybind11_plan.md)

## 1. Decision to implement

Align Python with the existing language-binding abstraction:

> One top-level LIME element produces one public language file. Nested LIME
> declarations remain nested in that element's public API.

For example, `InnerClassForwardDeclarations.lime` should expose one Python
module containing the `InnerClassForwardDeclarations` wrapper and its nested
types. The intended use is:

```python
from smoke.forward.InnerClassForwardDeclarations import InnerClassForwardDeclarations

InnerClassForwardDeclarations.InnerClass2.InnerInnerClass1
```

This is deliberately **not** a general one-`.lime`-file-to-one-module rule.
If one source file contains multiple top-level LIME elements, each top-level
element continues to get its own module, as it does for Java, Kotlin, Swift,
Dart, and C++.

The current Python generator is the outlier: it flattens nested names and
generates separate modules such as
`InnerClassForwardDeclarationsInnerClass2InnerInnerClass1.py`.

## 2. Constraints and invariants

- Preserve the LIME/C++ containment hierarchy in Python names.
- Preserve the existing C++ types and fully-qualified C++ references.
- Keep one CPython extension module (`generated`) and the current wrapper/cache
  model.
- Keep pybind11's current minimum version (`>= 2.11`) unless implementation
  evidence requires a change.
- Do not make nested classes require an enclosing Python instance. LIME nested
  declarations correspond to Python class attributes, not inner objects with an
  implicit outer reference.
- Keep top-level imports and public naming stable wherever possible.
- Keep internal and skipped declarations out of the public Python surface.
- Preserve registration-before-use requirements for C++ inheritance and
  pybind11 type casters.

## 3. Feasibility conclusion

pybind11 has the required native support. Its `py::class_` and `py::enum_`
constructors accept a parent scope:

```cpp
py::class_<Outer> outer(module, "Outer");
py::class_<Outer::Inner>(outer, "Inner");
py::enum_<Outer::Kind>(outer, "Kind");
```

The generated C++ already resolves nested C++ types correctly, for example
`Outer::Inner::Nested`. The work is therefore generator architecture and
registration orchestration, not a pybind11 capability gap.

The custom Gluecodium exception path is different: it uses exception
translators and `Return<T, Error>` registration rather than ordinary
`py::class_` bindings. Nested exceptions require a focused design and test
before being declared complete.

## 4. Current implementation gaps

1. `PythonGenerator.getPythonTypes()` flattens every nested type into the
   generation list.
2. `PythonNameRules` concatenates nested path segments, so `A.BC` and `AB.C`
   can collide as `ABC`.
3. Each pybind11 `register_*` function accepts only `py::module_&`, forcing every
   type into the extension module's root scope.
4. The module initializer calls every flattened registration function directly;
   it has no containment edges in its dependency graph.
5. Python templates and stubs describe each nested type as a top-level class in
   a separate file rather than as a member of its parent wrapper.
6. Existing generated wrappers refer to flat native attributes such as
   `generated.<package>_<Outer><Inner>`; scoped native registration needs either
   a resolver update or a transitional flat alias.
7. The output cache must remove obsolete flattened files when the new layout is
   generated.

## 5. Target architecture

### 5.1 Public Python files

Generate `.py` and `.pyi` files for top-level LIME elements only. Each file
contains the top-level wrapper plus recursively emitted nested declarations.

The first implementation may define nested wrappers under private module names
and attach them to the parent after both definitions exist:

```python
class _InnerClass2InnerInnerClass1(...):
    ...

InnerClass2.InnerInnerClass1 = _InnerClass2InnerInnerClass1
Outer.InnerClass2 = InnerClass2
```

This avoids Python class-body lookup and circular-definition problems. The
`.pyi` output should expose the natural nested declarations directly for type
checkers. A later cleanup can improve `__qualname__` if needed.

### 5.2 Native pybind11 scopes

Change nested registration to use the parent binding as scope. A conceptual
shape is:

```cpp
void register_Outer(py::module_& module) {
    py::class_<Outer> outer(module, "Outer");
    register_Outer_Inner(outer);
}

void register_Outer_Inner(py::handle scope) {
    py::class_<Outer::Inner>(scope, "Inner");
}
```

The exact registration type should be `py::handle` or another non-templated
scope type so one common declaration works for modules and parent
`py::class_` objects.

During migration, retain hidden flat extension aliases if that substantially
reduces resolver churn:

```cpp
module.attr("<flat-internal-name>") = outer.attr("Inner");
```

Those aliases are implementation compatibility, not public API, and should be
covered by a removal follow-up.

### 5.3 Registration dependencies

The registration graph must model two edge types:

- **Inheritance:** a C++ base must be registered before the derived
  `py::class_` is constructed.
- **Containment:** a child must be registered with an already-created parent
  scope.

Root registration functions should be invoked by `_module_init.cpp`. Nested
registration functions should be invoked from their parent registration path,
not independently from module initialization. Cycles should be rejected with a
diagnostic; LIME containment itself is expected to be acyclic.

## 6. Implementation phases

### Phase 0 — Baseline and API inventory

- Capture current generated output and functional-test imports for nested types.
- Enumerate nested classes, interfaces, structs, enums, exceptions, lambdas,
  and type aliases in the smoke and functional inputs.
- Record which existing imports are intended to remain compatible.
- Add a generator-level fixture with two potentially colliding flattened names:
  `A { struct BC }` and `AB { struct C }`.

**Exit criteria:** baseline is reproducible and all affected output files are
identified.

### Phase 1 — Model grouping and naming

- Keep `topElements` as the public-file generation units.
- Build a recursive nested-type tree from each top-level element.
- Change Python type names inside a parent scope to their own segment (`Inner`),
  while retaining a separate internal identifier for C++ registration and
  compatibility aliases.
- Make module/reference resolution return the top-level module for nested
  types.
- Remove the silent duplicate-file filtering; collisions should either become
  impossible under the new layout or produce an explicit validation error.

**Exit criteria:** one top-level Python file is generated per top-level LIME
element, and all nested references resolve to the correct parent module.

### Phase 2 — Scoped pybind11 registration

- Introduce a scope-agnostic registration signature.
- Generate parent-first nested registration calls.
- Extend dependency ordering with containment edges while preserving inheritance
  ordering.
- Keep the existing trampoline, holder, overload, and multiple-inheritance
  template logic unchanged initially.
- Add scoped enum registration using the existing `py::enum_` path; do not
  require `py::native_enum` or a pybind11 version upgrade.
- Decide whether to emit temporary flat native aliases.

**Exit criteria:** a compiled extension exposes `Outer.Inner` and nested enums
through the native `generated` module, with no registration-order failures.

### Phase 3 — Python wrappers and stubs

- Make `PythonClass`, `PythonInterface`, `PythonStruct`, `PythonEnumeration`,
  and related templates emit nested declarations recursively.
- Preserve wrapper construction, `_native` adoption, trampoline dispatch,
  return wrapping, and wrapper-cache behavior.
- Emit natural nested declarations in `.pyi` files.
- Ensure nested method signatures refer to sibling, parent, and deeply nested
  types without module-level circular imports.

**Exit criteria:** runtime wrappers and static stubs both expose the same nested
  hierarchy.

### Phase 4 — Exceptions and non-binding declarations

- Design how nested exceptions map to generated Python exception classes and
  the `Return<T, Error>` registry.
- Verify type aliases and lambdas remain declarations in the parent module and
  do not receive unnecessary native registration functions.
- Verify `@Internal`, `@Python(Skip)`, external types, and platform filtering
  work recursively.

**Exit criteria:** every nested LIME declaration kind has an explicit supported
  or rejected behavior with a diagnostic and test.

### Phase 5 — Compatibility and cache migration

- Decide whether flattened modules remain as generated compatibility shims for
  one release.
- If retained, make each shim re-export the nested symbol from the top-level
  module and mark it deprecated in documentation.
- Verify the output cache removes obsolete flattened files when shims are not
  enabled.
- Update CMake file lists and generated-source discovery if they assume one
  pybind11 source per flattened type.

**Exit criteria:** clean generation from an old output directory produces no
  stale or duplicate bindings, and the compatibility policy is documented.

### Phase 6 — Test and documentation rollout

- Regenerate smoke goldens for nested classes, structs, enums, interfaces, and
  exceptions.
- Add functional tests for nested runtime access and Python subclassing.
- Update imports in functional tests to use the new public hierarchy.
- Document the public Python naming rule and migration path.

**Exit criteria:** focused tests, smoke tests, and the Python functional suite
pass on supported platforms.

## 7. Required test matrix

- `InnerClassForwardDeclarations`: one-level and two-level nesting, forward
  references, internal nested declarations.
- Nested structs with fields, constructors, defaults, equality, and collections.
- Nested enums used as fields, parameters, return values, and constants.
- Nested interfaces/classes with Python trampolines and inherited methods.
- Nested types participating in multiple inheritance.
- Nested exceptions, including enum-backed and struct-backed errors.
- Same short nested name under different parents and packages.
- Flattening-collision regression (`A.BC` versus `AB.C`).
- Cross-file references to nested types.
- `@Internal`, `@Python(Skip)`, external declarations, and cache cleanup.
- `generated.Outer.Inner` native access and public
  `Outer.Inner` wrapper access.
- `__module__`, `__name__`, `__qualname__`, `isinstance`, and wrapper-cache
  referential equality where applicable.

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Parent/child registration order is wrong | Add containment edges and compile/runtime tests for deep nesting |
| Existing wrappers expect flat native attributes | Keep temporary native aliases or update resolver atomically |
| Nested Python definitions create annotation cycles | Use deferred annotations and private definitions with explicit attachment |
| Exception translators do not naturally accept class scopes | Keep exception registration separate and test it before enabling nested exceptions |
| Existing users import flattened modules | Generate compatibility shims for a deprecation period, if API policy permits |
| Old generated files survive in cached output | Add obsolete-file cache tests and force-regeneration instructions |
| Multiple top-level types share a source file | Retain top-level-element grouping; never derive public module identity solely from the source basename |

## 9. Definition of done

- Python public modules follow the same top-level-element rule as the other
  language bindings.
- Nested classes, interfaces, structs, and enums are accessible through their
  parent scopes at runtime and in `.pyi` files.
- Native pybind11 registration uses parent scopes and passes all ordering tests.
- Exception behavior is explicitly supported or rejected, with no silent
  flattening.
- No nested type is silently dropped because of a generated filename collision.
- Compatibility and cache behavior are documented and tested.
- Smoke and functional tests pass without requiring flattened nested-module
  imports.
