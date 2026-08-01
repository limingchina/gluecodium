# Refactoring Plan: One Top-Level LIME Element → One Python Output File

## Background

Currently the Python generator **flattens** every nested type into a separate top-level module. For example, `InnerClassForwardDeclarations.InnerClass2.InnerInnerClass1` (defined in [InnerClassForwardDeclarations.lime](../../gluecodium/src/test/resources/smoke/instances/input/InnerClassForwardDeclarations.lime)) generates a standalone file `InnerClassForwardDeclarationsInnerClass2InnerInnerClass1.py`.

This design has several problems:

1. **Ugly, unreadable names** — `InnerClassForwardDeclarationsInnerClass2InnerInnerClass1` is not a natural Python identifier.
2. **Name collision risk** — `PythonNameRules.getName()` concatenates all path-tail components with no separator ([line 40](../../gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonNameRules.kt#L40)), so `A.BC` and `AB.C` both become `ABC`. The generator then **silently drops** colliding files ([`getPythonTypes` duplicate-file-name filter](../../gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGenerator.kt#L488-L504)).
3. **Complex circular-import machinery** — `generatePythonFile()` has ~50 lines of bespoke logic for `selfModulePath`, `ancestorModulePaths`, and `childModulePaths` filtering to break import cycles that only exist because parent and child are in separate modules.
4. **Inconsistent with C++/Dart** — Both the C++ generator ([`CppGenerator.kt:129-133`](../../gluecodium/src/main/java/com/here/gluecodium/generator/cpp/CppGenerator.kt#L129)) and the Dart generator ([`DartGenerator.kt:224-278`](../../gluecodium/src/main/java/com/here/gluecodium/generator/dart/DartGenerator.kt#L224)) iterate `topElements` and emit one output file per top element, including all nested types. Python is the only generator that flattens.
5. **Contradicts Python's native nested-class support** — Python fully supports `class Outer: class Inner: ...`, accessed as `Outer.Inner`. pybind11 also supports binding nested types by using a parent `py::class_` as the child's scope.

### Previous attempt (commit `bcc79e1`, later reverted)

Commit `bcc79e1` ("Python file-based module grouping for pybind11 bindings") added:
- `resolveFileReferenceName()` in `PythonNameResolver` (using `LimeModel.fileNameMap`).
- `getPythonFileNameForFile()` / `getPythonStubFileNameForFile()` in `PythonNameRules`.
- A `{{#models}}…{{/models}}` loop wrapper in `PythonFile.mustache` / `PythonStub.mustache`.

But it **did not change** `PythonGenerator` to actually group elements and pass a `models` collection. The templates therefore emitted imports but skipped all bindings/classes. The subsequent revert fixed the breakage but did not invalidate the architecture.

### Decision

Refactor to **one top-level LIME element → one `.py` / `.pyi` module**, matching the C++/Dart pattern. Nested types become **physically nested Python class definitions** inside their parent's class body, preserving the LIME containment structure.

---

## Architecture Overview

### Before (current)

```
PythonGenerator.generate()
  └─ getPythonTypes(topElements)          ← flattens ALL types (top + nested) into a flat list
       └─ for each type:
            generatePythonFile(type)      ← one .py + .pyi per type
            generatePybind11File(type)     ← one .cpp per type
```

- `PythonNameRules.getName()` → flattened name (`OuterInner`).
- `PythonNameResolver.resolveReferenceName()` → module path `pkg.OuterInner`.
- `PythonImportResolver.createImport()` → `from pkg.OuterInner import OuterInner`.
- Complex circular-import filtering in `generatePythonFile()`.

### After (target)

```
PythonGenerator.generate()
  └─ for each topElement in topElements:
       generatePythonFile(topElement)     ← one .py + .pyi per top element
       generatePybind11File(topElement)   ← one .cpp per top element (Phase 2)
```

- `PythonNameRules.getName()` → **short name** (`Inner`), never flattened.
- `PythonNameResolver.resolveName(LimeType)` → **short name** for class definitions.
- `PythonNameResolver.resolveName(LimeTypeRef)` → **qualified name** (`Outer.Inner`) for type references.
- `PythonNameResolver.resolveReferenceName()` → module path based on **top-level element** (`pkg.Outer`).
- `PythonImportResolver.createImport()` → `from pkg.Outer import Outer`.
- No circular-import filtering needed (types in the same file don't import each other).

---

## Implementation Phases

### Phase 1: Python wrapper files (`.py` and `.pyi`)

#### 1.1 `PythonNameRules.kt`

**Change `getName()` to always return the short (own) name:**

```kotlin
// BEFORE
override fun getName(limeElement: LimeElement) =
    getPlatformName(limeElement as? LimeNamedElement)
        ?: if (limeElement is LimeType && limeElement.path.hasParent) {
            limeElement.path.tail.joinToString("")       // ← flattened name
        } else {
            sanitizeKeyword(super.getName(limeElement))  // ← short name
        }

// AFTER
override fun getName(limeElement: LimeElement) =
    getPlatformName(limeElement as? LimeNamedElement)
        ?: sanitizeKeyword(super.getName(limeElement))   // ← always short name
```

The base `NameRules.getName()` calls `ruleSet.getTypeName(limeElement.name)`, which applies the configured name-rule formatting (e.g. `UpperCamelCase`) to the element's own name — the last component of its path. This is the correct Python class name for both top-level and nested types.

**Add `getFlattenedName()` for pybind11 registration (keeps backward-compatible flat identifiers):**

```kotlin
fun getFlattenedName(limeElement: LimeNamedElement): String {
    val platformName = getPlatformName(limeElement)
    if (platformName != null) return sanitizeKeyword(platformName)
    return sanitizeKeyword(
        if (limeElement is LimeType && limeElement.path.hasParent)
            limeElement.path.tail.joinToString("")
        else
            super.getName(limeElement)
    )
}
```

This is used by `resolveRegisterName()` to produce unique, dot-free C++/pybind11 identifiers (e.g. `smoke_forward_OuterInner`).

#### 1.2 `PythonNameResolver.kt`

**`resolveName()` — differentiate class definitions from type references:**

The same `resolveName` helper is called from templates in two distinct contexts:

| Template context | What `resolveName` receives | Desired output |
|---|---|---|
| `class {{resolveName}}(...)` | `LimeType` (the model) | **Short name** (`Inner`) |
| `def foo() -> {{resolveName returnType}}` | `LimeReturnType` → `LimeTypeRef` → `LimeType` | **Qualified name** (`Outer.Inner`) |

The existing code routes both through the `is LimeType ->` branch. The fix is to **intercept `LimeTypeRef`** before it reaches `is LimeType`:

```kotlin
is LimeTypeRef -> {
    val actualType = element.type.actualType
    val typeName = when (actualType) {
        is LimeLambda -> resolveLambdaType(actualType)
        else -> resolveQualifiedTypeName(actualType)   // ← NEW: qualified name
    }
    if (element.isNullable) "Optional[" + typeName + "]" else typeName
}
```

And keep the `is LimeType` branch returning the short name:

```kotlin
is LimeType -> nameRules.getName(element)   // ← short name (after NameRules change)
```

**Add `resolveQualifiedTypeName()` helper:**

```kotlin
private fun resolveQualifiedTypeName(limeType: LimeType): String {
    if (!limeType.path.hasParent) return nameRules.getName(limeType)
    // Walk path.tail, look up each ancestor in the reference map, resolve its name.
    val head = limeType.path.head
    val tail = limeType.path.tail
    val sb = StringBuilder()
    var currentFullPath: String? = null
    for (component in tail) {
        currentFullPath = if (currentFullPath == null)
            head.joinToString(".") + "." + component
        else
            "$currentFullPath.$component"
        val element = limeReferenceMap[currentFullPath] as? LimeNamedElement
        val name = if (element != null) nameRules.getName(element) else component
        if (sb.isNotEmpty()) sb.append(".")
        sb.append(name)
    }
    return sb.toString()
}
```

**Change `resolveReferenceName()` to use the top-level element's module path:**

```kotlin
override fun resolveReferenceName(element: Any): String? {
    val limeType = when (element) {
        is LimeTypeRef -> element.type.actualType
        is LimeType -> element.actualType
        else -> return null
    }
    val namedType = limeType as? LimeNamedElement ?: return null
    val topLevel = findTopLevelElement(namedType) ?: namedType
    return (topLevel.path.head + nameRules.getName(topLevel)).joinToString(".")
}
```

**Add `findTopLevelElement()` helper:**

```kotlin
private fun findTopLevelElement(element: LimeNamedElement): LimeNamedElement? {
    var current = element
    while (current.path.hasParent) {
        val parent = limeReferenceMap[current.path.parent.toString()] as? LimeNamedElement
            ?: return current
        current = parent
    }
    return current
}
```

**Change `resolveRegisterName()` to use the flattened name:**

```kotlin
fun resolveRegisterName(limeElement: LimeNamedElement): String {
    val name = nameRules.getFlattenedName(limeElement)
    val packagePath = limeElement.path.head.joinToString("_")
    return if (packagePath.isNotEmpty()) "${packagePath}_$name" else name
}
```

#### 1.3 `PythonImportResolver.kt`

**Change `createImport()` to import the top-level element:**

```kotlin
private fun createImport(limeElement: LimeNamedElement): PythonImport {
    val topLevel = findTopLevelElement(limeElement) ?: limeElement
    val modulePath = (topLevel.path.head + nameResolver.resolveName(topLevel)).joinToString(".")
    return PythonImport(modulePath, nameResolver.resolveName(topLevel))
}
```

This produces `from pkg.Outer import Outer` instead of `from pkg.OuterInner import OuterInner`. Access to nested types is via attribute access: `Outer.Inner`.

The `findTopLevelElement()` helper needs access to the reference map. Currently `PythonImportResolver` has `limeReferenceMap` as a private field, so the helper can be added there, or the resolver can delegate to `PythonNameResolver`.

#### 1.4 `PythonGenerator.kt`

**Change `generate()` to iterate `topElements` instead of flattening:**

```kotlin
// BEFORE
val pythonTypes = getPythonTypes(pythonFilteredModel.topElements)
val pythonFiles = pythonTypes.flatMap { generatePythonFile(it, ...) }

// AFTER
val pythonFiles = pythonFilteredModel.topElements.flatMap {
    generatePythonFile(it, nameResolvers, predicates)
}
```

Only top-level elements are passed to `generatePythonFile()`. The template handles nested types recursively.

**Simplify `generatePythonFile()` — remove circular-import filtering:**

The entire `selfModulePath` / `ancestorModulePaths` / `childModulePaths` block (~50 lines) is no longer needed because all types from one top element are in the same file and don't import each other.

```kotlin
private fun generatePythonFile(
    limeElement: LimeNamedElement,
    nameResolvers: Map<String, NameResolver>,
    predicates: Map<String, (Any) -> Boolean>,
): List<GeneratedFile> {
    val imports = pythonImportsCollector.collectImports(limeElement)
        .filterNot { it.modulePath == selfModulePath }   // still drop self-import
        .distinct()
        .sorted()

    // Recursively generate the class body (including nested types)
    val contentBody = generateTypeBody(limeElement, nameResolvers, predicates)
    val stubBody = generateTypeStubBody(limeElement, nameResolvers, predicates)

    val templateData = mapOf(
        "content" to contentBody,
        "stubContent" to stubBody,
        "imports" to imports,
        "moduleName" to pythonModule,
        "nativeModule" to pythonModule,
        "usesCallable" to usesCallable(limeElement),
    )
    ...
}
```

**Add `generateTypeBody()` — recursive nested class generation with indentation:**

The core challenge is **Python's significant indentation**. Mustache partials (`{{>template}}`) insert content as-is without additional indentation. To handle arbitrary nesting depth, the generator recursively renders each type's class body and then **indents** the nested bodies before injecting them into the parent.

```kotlin
private fun generateTypeBody(
    element: LimeNamedElement,
    nameResolvers: Map<String, NameResolver>,
    predicates: Map<String, (Any) -> Boolean>,
    indent: String = "",
): String {
    // 1. Generate nested type bodies first (recursively)
    val container = element as? LimeContainer
    val nestedTypes = container?.let {
        (it.structs + it.classes + it.interfaces + it.enumerations + it.typeAliases + it.lambdas + it.exceptions)
            .filterNot { /* skip internal/skipped */ }
    } ?: emptyList()

    val nestedBodies = nestedTypes.map { nested ->
        generateTypeBody(nested, nameResolvers, predicates, "    ")
    }
    val nestedTypesStr = if (nestedBodies.isNotEmpty())
        "\n" + nestedBodies.joinToString("\n\n").prependIndent(indent + "    ")
    else
        ""

    // 2. Render THIS type's class body using its template
    val templateData = mapOf(
        "model" to element,
        "nativeModule" to pythonModule,
        "typeName" to pythonNameResolver.resolveRegisterName(element),
        "nestedTypes" to nestedTypesStr,
        "contentTemplate" to selectPythonTemplate(element),
        // ... other variables
    )
    return TemplateEngine.render("python/PythonClassBody", templateData, nameResolvers, predicates)
}
```

Kotlin's `String.prependIndent()` adds the given prefix to every line, which correctly shifts the entire nested class body by one indentation level.

#### 1.5 Template changes

**New template: `python/PythonClassBody.mustache`**

A "pure" class definition **without imports** (imports are handled at the file level):

```mustache
{{#ifPredicate model "needsTrampoline"}}
class {{resolveName}}({{nativeModule}}.{{typeName}}):
{{#ifPredicate this "hasAnyComment"}}    """{{resolveName comment}}"""
{{/ifPredicate}}
    def __init__(self, native=None):
        ...
{{#functions}}

{{>python/PythonFunction}}{{/functions}}
{{#properties}}

{{>python/PythonProperty}}{{/properties}}
{{#enumerations}}
{{#unlessPredicate "isStandaloneEnum"}}
{{>python/PythonEnumeration}}{{/unlessPredicate}}{{/enumerations}}
{{#constants}}

{{>python/PythonConstant}}{{/constants}}
{{{nestedTypes}}}
{{/ifPredicate}}
{{#unlessPredicate model "needsTrampoline"}}
class {{resolveName}}(...):
    def __init__(self, native):
        super().__init__(native)
{{#functions}}

{{>python/PythonFunction}}{{/functions}}
...
{{{nestedTypes}}}
{{/unlessPredicate}}
```

Key: `{{{nestedTypes}}}` (triple braces = unescaped) injects the pre-indented nested class bodies.

**Same pattern for: `PythonInterfaceBody.mustache`, `PythonStructBody.mustache`, `PythonStubClassBody.mustache`, `PythonStubInterfaceBody.mustache`, `PythonStubStructBody.mustache`.**

**Update `PythonFile.mustache` — add file-level imports, use `{{{content}}}`:**

```mustache
from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from typing import Optional
{{#usesCallable}}from typing import Callable
{{/usesCallable}}
import {{nativeModule}}

{{#imports}}
{{#importedName}}from {{modulePath}} import {{importedName}}
{{/importedName}}{{^importedName}}import {{modulePath}}
{{/importedName}}{{/imports}}

{{{content}}}
```

- `from _native_base import _NativeBase` and `import {{nativeModule}}` are now at the file level (previously inside each class template). This is harmless for files that don't use them (e.g. enum-only files) and avoids duplication.
- `{{{content}}}` replaces `{{#model}}{{include contentTemplate}}{{/model}}` — the content is pre-rendered by the generator with proper nesting and indentation.

**Same pattern for `PythonStub.mustache` — use `{{{stubContent}}}`.**

#### 1.6 Remove or simplify `getPythonTypes()`

The `getPythonTypes()` method (lines 473-504 of `PythonGenerator.kt`) that flattens all types and filters duplicates is **no longer needed** for Python file generation. It may still be needed for the pybind11 module init's `allBoundTypes` list — that can be replaced with `topElements` + `LimeTypeHelper.getAllTypes()` per top element.

#### 1.7 Predicates to simplify

The following predicates in `PythonGeneratorPredicates.kt` exist solely to handle circular imports caused by flattening. With nested types in the same file, these become unnecessary (but can be kept as no-ops for minimal disruption):

- `isAncestorField` — no longer needed (ancestor types are in the same file, no import required).
- `isAncestorReturnType` — same.
- `isAncestorProperty` — same.

The `PythonField.mustache` and `PythonFunction.mustache` templates use these predicates to emit deferred (local) imports. With one-file-per-top-element, type references to ancestors are just `Outer.Inner` — no import needed.

---

### Phase 2: Pybind11 binding files (`.cpp`)

The pybind11 side has two options:

#### Option A: Keep per-type pybind11 files (minimal change)

Keep the current per-type `.cpp` files and `register_*` functions. The only changes:
- `resolveRegisterName()` uses `getFlattenedName()` (Phase 1.2 above).
- `PythonNameResolver` constructor receives the `fileNameMap` (or top-element map) if needed.
- The Python wrapper references pybind11 types via `generated.FlattenedName` (unchanged).

**Pros:** Minimal disruption to pybind11 templates.
**Cons:** Still many `.cpp` files; pybind11 module doesn't reflect nesting.

#### Option B: One pybind11 file per top element with nested scopes (full alignment)

Generate one `.cpp` per top element. The `register_*` function registers the top-level type AND all nested types, using the parent's `py::class_` as the child's scope:

```cpp
void register_pkg_Outer(py::module_& module) {
    auto outer = py::class_<Outer, ...>(module, "Outer");
    // ... bind Outer's methods ...

    auto inner = py::class_<Outer::Inner, ...>(outer, "Inner");
    // ... bind Inner's methods ...

    auto innerInner = py::class_<Outer::Inner::InnerInner, ...>(inner, "InnerInner");
    // ...
}
```

This requires significant template rework — the current `Pybind11Class.mustache` emits a standalone `register_*` function per type. The new template would need to:
1. Emit all trampoline class definitions for the top element and its nested types.
2. Emit a single `register_*` function with chained scopes.

**Pros:** Clean module structure; `generated.Outer.Inner` works natively.
**Cons:** Large template rewrite; registration order matters (parent before child).

**Recommendation:** Start with **Option A** for Phase 1, then migrate to Option B in a follow-up.

---

### Phase 3: Smoke test reference updates

After the generator and template changes, regenerate smoke test references:

```bash
DUMP_ACTUAL_DIR=$(pwd)/gluecodium/src/test/resources/smoke ./gradlew :gluecodium:test
```

Expected changes for the `instances/forward` smoke test:

| Before | After |
|---|---|
| `InnerClassForwardDeclarations.py` | `InnerClassForwardDeclarations.py` (now contains all nested types) |
| `InnerClassForwardDeclarationsInnerClass1.py` | **deleted** |
| `InnerClassForwardDeclarationsInnerClass2.py` | **deleted** |
| `InnerClassForwardDeclarationsInnerClass2InnerInnerClass1.py` | **deleted** |
| `InnerClassForwardDeclarationsInnerClass2InnerInnerClass2.py` | **deleted** |
| `InnerClassForwardDeclarationsInnerInterface2.py` | **deleted** |
| `InnerClassForwardDeclarationsInnerInterface3.py` | **deleted** |

Same for `.pyi` files.

Expected `InnerClassForwardDeclarations.py` content:

```python
from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from typing import Optional

import generated


class InnerClassForwardDeclarations(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class InnerInterface2(_NativeBase):
        def __init__(self, native):
            super().__init__(native)

    class InnerInterface3(_NativeBase):
        def __init__(self, native):
            super().__init__(native)

    class InnerClass1(_NativeBase):
        def __init__(self, native):
            super().__init__(native)

        def getInnerInterface(self) -> InnerClassForwardDeclarations.InnerInterface1:
            ...

    class InnerClass2(_NativeBase):
        def __init__(self, native):
            super().__init__(native)

        class InnerInnerClass1(_NativeBase):
            def __init__(self, native):
                super().__init__(native)

            def foo(self) -> InnerClassForwardDeclarations.InnerClass2.InnerInnerClass2:
                return _wrap(self._native.foo(),
                    InnerClassForwardDeclarations.InnerClass2.InnerInnerClass2)

        class InnerInnerClass2(_NativeBase):
            def __init__(self, native):
                super().__init__(native)

            def bar(self, arg: InnerClassForwardDeclarations.InnerInterface2):
                ...
```

### Phase 4: Functional test updates

Update functional test Python files that import nested types:

**Before:**
```python
from smoke.forward.InnerClassForwardDeclarationsInnerClass2InnerInnerClass1 import InnerClassForwardDeclarationsInnerClass2InnerInnerClass1
```

**After:**
```python
from smoke.forward.InnerClassForwardDeclarations import InnerClassForwardDeclarations
# Access: InnerClassForwardDeclarations.InnerClass2.InnerInnerClass1
```

---

## Key Design Decisions

### Why "one top element" not "one lime file"?

The C++ and Dart generators iterate `topElements`, not files. A single `.lime` file can contain multiple top-level types. Matching this pattern (one output per top element) is simpler and more consistent with the rest of the codebase.

### Why physically nested classes, not flat definitions + assignment?

Two alternatives were considered:

1. **Flat definitions + nesting assignments:**
   ```python
   class Outer_Inner(_NativeBase): ...
   Outer.Inner = Outer_Inner
   ```
   - Pros: No indentation challenge.
   - Cons: `__name__` is wrong; type checkers don't see `Outer.Inner` as an attribute; ugly internal names; requires `__name__`/`__qualname__` fixup.

2. **Physically nested class definitions:**
   ```python
   class Outer(_NativeBase):
       class Inner(_NativeBase): ...
   ```
   - Pros: Natural Python; correct `__name__`/`__qualname__`; type checkers understand nesting.
   - Cons: Mustache can't auto-indent; requires generator-side indentation handling.

**Decision:** Use physically nested classes. The indentation challenge is handled by generating each type's body as a string via `TemplateEngine.render()`, then using Kotlin's `String.prependIndent()` to shift the entire body before injecting it as a `{{{nestedTypes}}}` variable into the parent's template. This is a clean separation: templates define structure, the generator handles indentation.

### Why keep flattened names for pybind11 registration?

pybind11 registration names must be valid C++ identifiers (no dots). The Python wrapper uses `{{nativeModule}}.{{typeName}}` to reference the pybind11-bound class. For nested classes, `typeName` is `resolveRegisterName(element)` which returns `pkg_OuterInner` (flattened, dot-free). The Python class name (`{{resolveName}}`) is the short name (`Inner`), and the nesting is provided by the class body. The pybind11 type is an implementation detail; users interact with the Python wrapper, not the raw pybind11 module.

---

## Files to Change

| File | Change |
|---|---|
| `PythonNameRules.kt` | `getName()` → always short name; add `getFlattenedName()` |
| `PythonNameResolver.kt` | Qualify `LimeTypeRef` names; `resolveReferenceName()` → top-level module path; `resolveRegisterName()` → flattened; add `resolveQualifiedTypeName()`, `findTopLevelElement()` |
| `PythonImportResolver.kt` | `createImport()` → import top-level element |
| `PythonGenerator.kt` | Iterate `topElements`; simplify `generatePythonFile()`; add `generateTypeBody()` / `generateTypeStubBody()`; remove/simplify `getPythonTypes()` |
| `PythonGeneratorPredicates.kt` | `isAncestorField/ReturnType/Property` can become no-ops (Phase 2 cleanup) |
| `PythonFile.mustache` | File-level imports; `{{{content}}}` |
| `PythonStub.mustache` | File-level imports; `{{{stubContent}}}` |
| **New:** `PythonClassBody.mustache` | Class def without imports; `{{{nestedTypes}}}` |
| **New:** `PythonInterfaceBody.mustache` | Same pattern |
| **New:** `PythonStructBody.mustache` | Same pattern |
| **New:** `PythonStubClassBody.mustache` | Same pattern |
| **New:** `PythonStubInterfaceBody.mustache` | Same pattern |
| **New:** `PythonStubStructBody.mustache` | Same pattern |
| `PythonClass.mustache` | Simplified to delegate to `PythonClassBody` (or replaced) |
| `PythonInterface.mustache` | Same |
| `PythonStruct.mustache` | Same |
| `PythonStubClass.mustache` | Same |
| `PythonStubInterface.mustache` | Same |
| `PythonStubStruct.mustache` | Same |
| Smoke test references (`instances/forward`, etc.) | Regenerate |
| Functional test Python files | Update imports |

---

## Risk Assessment

1. **Indentation correctness** — The most fragile part. `prependIndent()` must handle blank lines and trailing whitespace correctly. Thorough testing of deeply nested types (2+ levels) is essential.

2. **Template variable scope** — When rendering nested type bodies separately, the Mustache context stack changes. Variables like `{{nativeModule}}`, `{{typeName}}`, `{{contentTemplate}}` must be passed explicitly in the per-type `templateData` map.

3. **Predicate context** — Predicates like `needsTrampoline`, `isInterface`, `hasAnyComment` are evaluated with the current Mustache context. When rendering a nested type body, the context must be the nested type itself (not the parent). `TemplateEngine.render()` resets the context for each call, so this should work correctly.

4. **Forward references** — In Python, `from __future__ import annotations` makes all annotations strings (lazy evaluation), so type hints can reference types defined later in the same file. However, runtime references (e.g., `_wrap(self._native.foo(), Outer.Inner)`) require the referenced class to be defined before the method is called. Since Python class bodies are executed top-to-bottom, a child class referencing a sibling defined later would fail at runtime. The LIME model typically orders types so that referenced types come first, but this needs verification.

5. **Smoke test scope** — There are many smoke test directories beyond `instances/forward`. All Python output files will change (imports, class structure). The `DUMP_ACTUAL_DIR` regeneration approach handles this, but the diff will be large.

---

## Validation Steps

1. **Unit tests:** `./gradlew :gluecodium:test` — smoke tests compare generated output against reference files.
2. **Regenerate references:** `DUMP_ACTUAL_DIR=$(pwd)/gluecodium/src/test/resources/smoke ./gradlew :gluecodium:test`
3. **Inspect output:** Manually verify `InnerClassForwardDeclarations.py` has nested classes with correct indentation.
4. **Functional tests:** `functional-tests/scripts/build-python-functional --publish` (after Phase 3 updates).
5. **Python import test:** `python3 -c "from smoke.forward.InnerClassForwardDeclarations import InnerClassForwardDeclarations; print(InnerClassForwardDeclarations.InnerClass2.InnerInnerClass1)"`
