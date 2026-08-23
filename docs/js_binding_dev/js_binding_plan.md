# Gluecodium JavaScript/WebAssembly Generator Plan (embind Approach)

> **Status**: Design phase
> **Author**: l2ming (plan drafted with Claude)
> **Date**: 2026-08-16
> **Base branch analyzed**: `limingchina/gluecodium` @ `python_bind` (commit `6d0c3ac`, "Emit `@typing.overload` in generated .pyi stubs for overloaded functions")
> **Related**: Follows the same architectural precedent as `docs/python_pybind11_plan.md`
> (Dart FFI / Swift CBridge / Python pybind11 generators used as reference implementations)
>
> **Reference implementation location**: The Python binding implementation lives in a **separate
> checkout at `~/dev/gluecodium1`** — a directory parallel to this project's folder
> (`~/dev/gluecodium`). During development, use it directly for code search and reference
> (e.g. `grep`/read `~/dev/gluecodium1/gluecodium/src/main/java/com/here/gluecodium/generator/python/`
> when mirroring `PythonGenerator` structure), rather than relying on the summarized snippets in
> this plan.

---

## 1. Background and Motivation

Gluecodium currently ships six generators (verified from
`gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator`
on `python_bind`):

```
com.here.gluecodium.generator.cpp.CppGenerator
com.here.gluecodium.generator.java.JavaGenerator
com.here.gluecodium.generator.swift.SwiftGenerator
com.here.gluecodium.generator.dart.DartGenerator
com.here.gluecodium.generator.kotlin.KotlinGenerator
com.here.gluecodium.generator.python.PythonGenerator
```

None of these targets JavaScript, TypeScript, or WebAssembly. A `js`/`embind` generator would let
the HERE SDK core (and any LimeIDL-defined API) run in browsers and Node.js by compiling the C++
core to WebAssembly via Emscripten and exposing it through
[embind](https://emscripten.org/docs/porting/connecting_cpp_and_javascript/embind.html).

### 1.1 Approach Selection: embind

| Approach | Advantages | Disadvantages |
|----------|------------|----------------|
| **Raw C-ABI shim via Emscripten `ccall`/`cwrap`** (reuse the existing `cbridge` C layer that Swift already uses) | Reuses a proven, already-generalized C-ABI shim; smallest new-technology surface | Manual marshalling of strings/vectors/structs/optionals across the JS↔wasm boundary in raw C, exactly what `cbridge` + Swift/Dart hand-roll today — no automatic container conversion, no automatic memory management, large amount of new hand-written glue for a modern JS API |
| **WebIDL Bindings** | Was Emscripten's original "structured" binding tool | Deprecated and removed from upstream Emscripten in favor of embind — not a viable target for new work |
| **embind** ✅ | Automatically converts `std::string`, `std::vector`, `std::map`; binds classes, enums, and overloaded methods directly from C++ with `EMSCRIPTEN_BINDINGS { ... }` blocks; ships inside the Emscripten SDK (no external package manager dependency, unlike pybind11); is the actively maintained, canonical Emscripten binding tool | No native multiple inheritance; no automatic garbage collection of wasm-heap objects (JS must call `.delete()`); requires the whole dependency graph to be cross-compiled through `emcc`/`em++`, not just the binding layer |

**Reasons for choosing embind** (mirrors the reasoning already used for pybind11 in
`docs/python_pybind11_plan.md` §1.1): it binds C++ classes directly, minimizes generated glue code,
and handles STL container/string conversion automatically. The main open risk — no multiple
inheritance — is called out explicitly in §5.3 and §4 below, because it directly affects a LimeIDL
pattern this codebase already has a functional test for.

### 1.2 Architecture Comparison

```
Existing Dart architecture:
  LimeIDL → LIME Model → DartGenerator
    ├── Dart code (dart:ffi calls)
    └── FFI C++ code (C-ABI shim → C++ API)

Existing Swift architecture:
  LimeIDL → LIME Model → SwiftGenerator
    ├── Swift code
    └── CBridge C/C++ code (C-ABI shim → C++ API)

Existing Python architecture (pybind11):
  LimeIDL → LIME Model → PythonGenerator
    ├── Python code (.py + .pyi type stubs)
    └── pybind11 C++ code (wraps the C++ API directly, no C-ABI intermediate layer)

New JavaScript/WebAssembly architecture (embind):
  LimeIDL → LIME Model → JsGenerator
    ├── TypeScript/JS glue (.d.ts type stubs; thin ES module wrapper, if any)
    └── embind C++ code (EMSCRIPTEN_BINDINGS blocks, wraps the C++ API directly,
        no C-ABI intermediate layer) → cross-compiled by `em++` into a
        `.wasm` binary + a JS "glue"/loader file
```

**Key similarity to pybind11**: like Python, embind does not need a `cbridge`-style C-ABI
intermediate layer — the generated `.cpp` binding files `#include` the C++ headers and call the
C++ API directly.

**Key difference from *every* existing target, including pybind11**: pybind11 produces a native
extension module that is dynamically loaded into an *already-running* CPython interpreter that was
built separately. embind instead requires the *entire* dependency graph — HERE SDK core, the
generated C++ layer, and the embind glue — to be compiled together by the Emscripten toolchain
(`em++`) into one `.wasm` artifact. There is no "generate glue, link against a pre-existing
runtime" story. This is the single biggest process/toolchain departure and drives most of the
risk in §4 and the build-integration work in Phase 7.

---

## 2. Implementation Phases

### Phase 0 — Prerequisites (spike, must gate Phase 2)

#### 0.1 Confirm Emscripten SDK version and toolchain shape
- Emscripten (`emsdk`) >= 3.1.51 recommended — this is roughly where embind's `optional<T>`
  registration helper and JS `BigInt`-based 64-bit integer support stabilized; confirm against the
  emsdk version actually pinned for HERE SDK's other wasm-adjacent tooling, if any.
- Unlike pybind11 (`find_package(pybind11 CONFIG REQUIRED)` in `cmake/modules/gluecodium/Python.cmake`),
  embind ships *inside* Emscripten itself (`<emscripten/bind.h>`, `<emscripten/val.h>`) — no
  separate package to locate, but the whole build must run under `emcmake`/`em++` rather than the
  host compiler.

#### 0.2 Spike: multiple-inheritance compatibility (go/no-go)
`functional-tests/functional/input/lime/MultipleInheritance.lime` defines:
```lime
class MultiClass: OpenClass, NarrowInterface { ... }
interface MultiInterface: RegularInterface, NarrowInterface { ... }
```
and every existing generator (Java/Kotlin, Swift, Dart, and Python via pybind11) has a passing
functional test for this file (see `functional-tests/functional/{android,android-kotlin,swift,dart}`
and the pybind11-based Python equivalent). `embind::class_<Derived, base<Base>>` accepts **exactly
one** base class template argument — there is no variadic multi-base form the way pybind11's
`py::class_<Derived, Base1, Base2>` has. This is the same structural requirement that led to
picking pybind11 over nanobind for the Python target; embind has the same limitation nanobind has.

Before committing to Phase 2, spike a minimal `MultiClass`/`MultiInterface`-shaped embind binding
and confirm the mitigation in §5.3 (primary-base registration + explicit upcast helpers, mirroring
the `getMultiClassAsNarrow()`/`upcastMultiInterfaceToNarrow()` static factory functions already
present in the `.lime` fixture) produces correct, referentially-equal objects on the JS side. If it
doesn't, this needs to be flagged as a known gap in generator parity, not silently worked around.

#### 0.3 Spike: minimal `emcmake` build of an existing example
Build `examples/calculator` (or a trivial subset) end-to-end through `emcmake cmake` + `emmake make`
to validate that the existing generated C++ output (headers, generated abstract classes, runtime)
compiles cleanly under `em++` without host-only constructs. This should surface any `-fexceptions`,
RTTI, or threading assumptions in the generated C++ / `lime-runtime` code before Phase 2 begins.

---

### Phase 1 — LIME Model Layer Extensions

#### 1.1 Add the `JS` attribute type

**File**: `lime-runtime/src/main/java/com/here/gluecodium/model/lime/LimeAttributeType.kt`

```kotlin
// Add to the enum, alongside JAVA / KOTLIN / SWIFT / DART / PYTHON:
JS("Js", LimeAttributeValueType.NAME),
```

This mirrors the existing convention: the attribute name tracks the **output language**
(`Dart`, `Swift`, `Python`), not the binding *technology* (`dart:ffi`, `cbridge`, `pybind11`).
embind is the technology; JavaScript/TypeScript is the language, so `@Js` — not `@Embind` — is the
attribute name recommended here (also see Open Question Q1 in §8).

```lime
@Js(Name = "customName")
class MyClass { ... }

@Js(Skip)
class InternalOnly { ... }

@Js(Internal)
fun internalMethod() { ... }
```

#### 1.2 Update the annotation converter

**File**: `lime-loader/src/main/java/com/here/gluecodium/loader/AntlrLimeConverter.kt`

Add to `convertAnnotationType()` (currently at line 315 on `python_bind`, alongside `"Python" ->
LimeAttributeType.PYTHON`):
```kotlin
"Js" -> LimeAttributeType.JS
```

Add `JS` to the `propagateParentAttributes()` traversal list (currently line 160):
```kotlin
listOf(JAVA, SWIFT, DART, KOTLIN, PYTHON, JS).forEach { ... }
```

#### 1.3 Add JS/TS naming rules

**New file**: `gluecodium/src/main/resources/namerules/js.properties`

Unlike Python's `snake_case`, JS/TS convention favors `camelCase` (closer to Dart/Kotlin than to
Python):
```properties
field=camelCase
parameter=camelCase
constant=UPPER_SNAKE_CASE
enumerator=UPPER_SNAKE_CASE
method=camelCase
property=camelCase
type=UpperCamelCase
error=UpperCamelCase
error.suffix=Error
join.infix=
```

#### 1.4 Update `GeneratorOptions`

**File**: `gluecodium/src/main/java/com/here/gluecodium/generator/common/GeneratorOptions.kt`

Add JS-related option fields, following the existing `pythonPackages` / `pythonModule` pattern
(currently lines 74–81):
```kotlin
var jsPackages: List<String> = listOf(),
var jsInternalPackages: List<String> = listOf(),
var jsNameRules: Configuration = ConfigurationProperties.fromResource(
    Gluecodium::class.java, "/namerules/js.properties"
),
var jsModuleName: String = "generated",  // Emscripten Module factory / EMSCRIPTEN_BINDINGS module name
var jsEmitTypeScriptStubs: Boolean = true,
```

#### 1.5 CLI option support

**File**: `gluecodium/src/main/java/com/here/gluecodium/cli/OptionReader.kt`

Following the `pythonpackage` / `pythonmodule` / `pythonnamerules` pattern (lines 149–157,
294–298):
```kotlin
addOption("jspackage", true, "JS/TS package (namespace) for generated sources")
addOption("jsintpackage", "js-internal-package", true,
    "JS/TS sub-package to append to 'jspackage' for internal types.")
addOption("jsmodule", true, "Name of the generated Emscripten module / embind binding namespace")
addOption("jsnamerules", true, "JS name rules property file.")
```
with corresponding `generatorOptions.js*` assignments mirroring lines 294–298.

> Pulling the CLI/options wiring into Phase 1 (rather than deferring to a later "Phase 2.4"-style
> slot) worked well for Python — see the "Status" note under §1.4 of
> `docs/python_pybind11_plan.md` — and is recommended here too, since it's low-risk and unlocks
> end-to-end smoke testing earlier.

---

### Phase 2 — Generator Skeleton

#### 2.1 Create the JS generator package

```
gluecodium/src/main/java/com/here/gluecodium/generator/js/
├── JsGenerator.kt                  # Main generator class, implements the Generator interface
├── JsNameResolver.kt               # LIME → JS/TS name resolution
├── EmbindNameResolver.kt           # LIME → C++ embind name resolution (parallels Pybind11NameResolver.kt)
├── JsCommentsProcessor.kt          # LIME docs → JSDoc/TSDoc comments (parallels PythonCommentsProcessor.kt)
├── JsGeneratorPredicates.kt        # Template predicates (parallels PythonGeneratorPredicates.kt)
├── JsImport.kt / JsImportResolver.kt / JsImportsCollector.kt   # TS import statement handling
├── EmbindIncludeResolver.kt        # #include resolution for embind .cpp files (parallels Pybind11IncludeResolver.kt)
├── JsNameRules.kt
└── package-info.java
```

This is a direct structural mirror of `gluecodium/src/main/java/com/here/gluecodium/generator/python/`
(12 files on `python_bind`), which itself mirrors the Swift/`cbridge` split: one name-resolver pair
per language boundary (JS-facing vs. C++-facing), one imports/includes collector pair, comments
processor, and predicates.

#### 2.2 Implement the `JsGenerator` class

Follow `PythonGenerator.kt`'s structure closely (it is 808 lines on `python_bind` and is the
closest analog, since it also has no C-ABI intermediate layer):

- **Dual model filtering**, same rationale as `PythonGenerator.generate()` (lines 93–121):
  - an `embindFilteredModel` that retains functions/fields (`retainFunctionsAndFields = true`) for
    generating the embind C++ binding bodies, and additionally must **not** skip C++-external
    types (mirroring the "does NOT skip external types" comment at lines 99–105 of
    `PythonGenerator.kt` — the same reasoning applies: embind still needs to `#include` and bind
    external C++ types referenced by other bound types).
  - a `jsFilteredModel` for the actual `.d.ts`/`.js` output (`retainFunctionsAndFields = false`).
- `@Internal` handling: decide whether JS follows Python's convention (retain, but rename with a
  leading underscore / `#`-private field convention) or C++-skip semantics used elsewhere. TS has
  a native `private`/`#field` story that Python's leading-underscore convention doesn't, so this
  is worth a short design note rather than copying Python's approach blindly.
- Respect `@Cpp(Skip)` the same way `PythonGenerator.isCppSkipped()` does (lines 801–803): field
  constructors/constants skipped in C++ must not be emitted as embind `class_::constructor<...>()`
  calls either, for the same "would fail to compile" reason.

#### 2.3 Register the generator

**File**: `gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator`

```
com.here.gluecodium.generator.cpp.CppGenerator
com.here.gluecodium.generator.java.JavaGenerator
com.here.gluecodium.generator.swift.SwiftGenerator
com.here.gluecodium.generator.dart.DartGenerator
com.here.gluecodium.generator.kotlin.KotlinGenerator
com.here.gluecodium.generator.python.PythonGenerator
com.here.gluecodium.generator.js.JsGenerator
```

`shortName = "js"` (CLI: `-g js`, matching the `-g python` convention), keeping the "attribute
name = language = generator short name" convention rather than naming the generator `embind`.

---

### Phase 3 — Template System

#### 3.1 Create Mustache templates

**New directory**: `gluecodium/src/main/resources/templates/js/`

Mirror the Python template set (`templates/python/Pybind11Class.mustache`,
`PythonClass.mustache`, `PythonStubClass.mustache`, etc.) with three parallel families per LIME
type (`Class`, `Interface`, `Struct`, `Enumeration`, `Exception`, `Lambda`, `TypeAlias`):

- `Js*.mustache` — any hand-written JS wrapper code, if needed beyond the raw Emscripten glue.
- `JsStub*.mustache` — `.d.ts` TypeScript declaration files (parallels `PythonStub*` → `.pyi`).
- `Embind*.mustache` — the C++ `EMSCRIPTEN_BINDINGS` registration code (parallels `Pybind11*` →
  pybind11 `py::class_<...>` registration).

#### 3.2 embind binding template example (conceptual)

```cpp
#include <emscripten/bind.h>
#include "{{headerInclude}}"

using namespace emscripten;

void register_{{name}}(void) {
    class_<{{cppFullName}}, base<{{primaryCppBase}}>>("{{jsName}}")
        {{#constructors}}
        .constructor<{{paramTypes}}>()
        {{/constructors}}
        {{#methods}}
        .function("{{jsMethodName}}", &{{cppFullName}}::{{cppMethodName}})
        {{/methods}}
        {{#properties}}
        .property("{{jsPropertyName}}", &{{cppFullName}}::{{cppGetter}}{{#hasSetter}}, &{{cppFullName}}::{{cppSetter}}{{/hasSetter}})
        {{/properties}}
        ;
}
```

Note the single `base<...>` slot — see §5.3 for how multi-parent LIME types map onto this.

#### 3.3 TypeScript stub template example (conceptual)

```typescript
export class {{jsName}} {
  {{#constructors}}
  constructor({{paramList}});
  {{/constructors}}
  {{#methods}}
  {{jsMethodName}}({{paramList}}): {{returnType}};
  {{/methods}}
  {{#properties}}
  {{jsPropertyName}}: {{propertyType}};
  {{/properties}}
  delete(): void;   // explicit manual free — see §5.1
  [Symbol.dispose](): void; // using-compatible alias for delete()
}
```

---

### Phase 4 — Type Mapping

#### 4.1 Basic type mapping

| LIME type | C++ type | JS/TS type |
|-----------|----------|------------|
| `Boolean` | `bool` | `boolean` |
| `Int`/`UInt` | `int32_t`/`uint32_t` | `number` |
| `Long`/`ULong` | `int64_t`/`uint64_t` | `bigint` (requires `-sWASM_BIGINT`, see §4.5) |
| `Float`/`Double` | `float`/`double` | `number` |
| `String` | `std::string` | `string` |
| `Byte` | `int8_t` | `number` |

#### 4.2 Compound type mapping

- `List<T>` → `std::vector<T>` → requires an explicit `emscripten::register_vector<T>("VectorT")`
  call per instantiated element type (unlike pybind11, where `std::vector<T>` conversion is
  largely automatic via `pybind11/stl.h`). The generator needs to collect every distinct `vector<T>`
  instantiation across the model and emit one `register_vector` call per type, analogous to how
  `PythonImportsCollector`/`GenericImportsCollector` already collects distinct type references —
  reuse that collection pass rather than building a new one.
- `Map<K, V>` → `std::map<K, V>` → same story via `emscripten::register_map<K, V>("MapKV")`.
- `Optional<T>` → **risk area**: embind has no first-class `std::optional<T>` binding the way
  pybind11's `pybind11/stl.h` does. Needs either (a) a hand-written value-type caster (same shape
  as the Python `Pybind11Chrono`-style spike described in
  `docs/python_binding_dev/spike_chrono_caster.md`) that maps to a JS `T | null`/`T | undefined`,
  or (b) waiting on/adopting whatever `optional<T>` helper the target Emscripten version ships.
  This should get its own spike doc (`docs/js_binding_dev/spikes/optional_caster_spike/README.md`) before Phase 4
  is marked done, mirroring how the Python plan spiked its chrono/return casters separately.

#### 4.3 User-defined type mapping

- `class`/`interface` → `embind::class_<T>`
- `enum` → `embind::enum_<T>`
- `struct` (value type) → `embind::value_object<T>` (not `class_`) where all-fields-public value
  semantics apply — this is a genuine embind feature with no direct pybind11 equivalent to copy
  from; needs its own design note plus functional-test coverage (LIME `struct` already has one in
  every other generator).

#### 4.4 64-bit integers and `BigInt`

JS `number` is IEEE-754 double (53-bit safe integer range). Modern Emscripten (`-sWASM_BIGINT`)
maps C++ `int64_t`/`uint64_t` to JS `bigint` instead of silently truncating. This must be a
required link flag, not optional, or any LIME `Long`/`ULong` field will silently corrupt values
above 2^53 — flag as a hard requirement in Phase 7, and add it to the acceptance criteria in §6.

#### 4.5 Minimal build integration harness (dev-only, immediately after Phase 4)

**Decision (2026-08-22): formalize the Phase 0.3 spike into a repeatable
`generate → emcmake → node` loop as soon as Phase 4 lands — do not wait for full Phase 7.**

Rationale: functional-style verification for this target requires compiling generated embind
`.cpp` + C++ under `em++` and executing the `.wasm` in Node.js, so there is otherwise no runnable
artifact to test against until Phase 7 exists. A *minimal* harness needs only:

1. A small CMake project that:
   - Runs Gluecodium with `-generators cpp,js` on the test `.lime` files (via the `generate`
     launcher or Gradle plugin),
   - Configures with `emcmake` so everything compiles under `em++`,
   - Links one module with only the essential flags:
     `-lembind -fexceptions -sMODULARIZE=1 -sEXPORT_ES6=1 -sALLOW_MEMORY_GROWTH=1`.
2. A Node.js script that loads the module and asserts a few values.
3. Optionally, a shell script tying the three steps together.

**This is explicitly *not* a throw-away project**: it is a standing development harness, kept in
use from right after Phase 4 until full Phase 7 build integration (§7.2 `Js.cmake`) lands and
supersedes it. It is the primary correctness signal for all generator work during Phases 4–7
(templates, type mapping, lifecycle, output layout), extended incrementally as later phases add
features — it is only "minimal" in what it covers, not in its lifespan.

This is enough surface for meaningful assertions once Phase 4's type mapping lands (structs via
`value_object`, optionals, containers, strings, enums all round-trip). It deliberately excludes
everything else from Phase 7: no `Js.cmake`, no functional-tests CMake integration, no
pthreads/`PROXY_TO_PTHREAD`, no cross-origin-isolation story, no browser pass.

Benefits: template errors, bad includes, and name-resolution bugs in generated `.cpp` surface as
compile errors immediately instead of piling up until Phase 7; by the time `Js.cmake` is written,
the required flags and output-layout behavior are known empirically, making real Phase 7 mostly
mechanical.

Caveats:
- Keep it lightweight and clearly-marked as a dev-only harness (whether in-repo under a dedicated
  directory or as a scratch location) so it does not compete with `Js.cmake` once Phase 7 lands;
  at that point it is retired in favor of the real integration and §7.4's calculator example.
- Smoke tests remain deferred per §8.1 (golden reference files are generated only after all
  functional tests pass); this harness serves the functional-verification role during development
  only.
- Phase 5 features (callbacks, JS-implemented interfaces, disposal) will require extending the
  harness incrementally — expected, not a redesign.
- This does **not** replace §7.4: the calculator example still becomes a first-class generated-JS
  example only after full Phase 7 lands.

---

### Phase 5 — Object Lifecycle and Callbacks

#### 5.1 Object lifecycle management — the biggest departure from every existing target

Every existing target has some form of automatic reclamation on the platform side: Java/Kotlin GC,
Swift ARC, Dart GC, and CPython refcounting for pybind11. **JavaScript's garbage collector does
not know about the wasm heap.** A JS wrapper object returned by embind holds a pointer into wasm
linear memory; if the JS wrapper is GC'd without an explicit `.delete()` call, the underlying C++
object (and its wasm-heap memory) leaks.

Two mechanisms are planned, but the safety-net default depends on the module's
threading mode:
1. **Explicit `dispose()`/`delete()` contract** (embind's native behavior) — every generated class
   gets a `.delete()` method (already sketched in the stub template in §3.3); this is the safe,
   deterministic default and should be the primary documented contract.
2. **`FinalizationRegistry`-based best-effort safety net** — register each JS wrapper with a
  `FinalizationRegistry` that evicts generated cache metadata when the JS object is GC'd. This is explicitly
  non-deterministic (the spec gives no timing guarantee) and should be pitched as a leak-reducing
  safety net only, never as a replacement for explicit disposal. The registry is implemented in
  the generated JavaScript wrapper layer, but it is enabled by default only for configurations
  with a verified same-thread cleanup path. Pthread builds keep it opt-in until cross-thread
  marshalling is implemented and tested; an arbitrary finalizer callback must never call
  `emscripten::val` or embind deletion from the wrong thread.

Generated TypeScript declarations also expose `[Symbol.dispose]()` as an additive alias for
`.delete()`. On runtimes implementing the Explicit Resource Management proposal, this enables
`using` declarations to perform deterministic cleanup. It does not replace `.delete()`: browser
support varies, and consumers may need an `ESNext.Disposable` TypeScript library configuration.

The generated `js/WrapperRuntime.mjs` layer is the single lifecycle integration point for the
cache, explicit deletion interception, `[Symbol.dispose]`, and finalization. These concerns must
not be implemented as independent mechanisms: cache eviction and any finalizer cleanup must use
the same ownership and thread-affinity rules.

Consumers apply the generated layer to the Emscripten module factory result with
`wrapModule(await createModule())`. The runtime patches only generated class and interface
exports; enum, struct, and other value exports remain untouched.

Its intended flow is: embind creates a candidate handle for a shared-pointer return; the generated
layer looks up the `(native pointee address, exposed embind type)` key; a live canonical wrapper is
returned when present and the duplicate candidate is released; otherwise the candidate becomes the
canonical wrapper. The generated `.delete()` evicts the key, marks the wrapper disposed, and
delegates to the underlying embind handle exactly once. `[Symbol.dispose]()` calls that same path.
The generated layer owns JavaScript cache bookkeeping, while embind's `std::shared_ptr` holder
remains the native owner. Any `FinalizationRegistry` callback must use the same eviction path and
must be disabled or marshalled for pthread configurations where its callback can run off-thread.
The current generated registry only evicts weak cache metadata and never calls `.delete()` or
accesses `emscripten::val`; embind's own finalization path remains responsible for native-holder
cleanup. It is opt-in via `enableFinalization` until a stronger lifecycle hook is available.

For functions returning pointers to existing (non-owned) C++ objects, decide the embind equivalent
of pybind11's `return_value_policy::reference_internal` vs. `take_ownership` — embind's smart
pointer holder (`.smart_ptr<std::shared_ptr<T>>()`) is the natural fit given the codebase's
existing `std::shared_ptr`-centric object model (see `docs/pointer_equality.md`: interface
implementations passed from platform code to C++ are already wrapped in `std::shared_ptr` for
exactly this reason).

#### 5.2 Referential Equality

Per `docs/pointer_equality.md`, Gluecodium's existing bindings already solve half of this problem:
a C++ object wrapped by platform code is never copied, so the C++-side pointer is stable; the
*platform*-side wrapper is what risks going stale on re-retrieval. embind needs the same
`C++ pointer → JS object` wrapper cache the Dart `InstanceCache`/Swift `WrapperCache`/Python
`_wrapper_cache.h` implementations already provide (`PythonNameRules.PYBIND11_TARGET_DIRECTORY +
"_wrapper_cache.h"`, generated by `PythonGenerator.kt` line ~677). The Phase 5 spike confirmed
that embind does not canonicalize ordinary smart-pointer return wrappers. The implementation must
therefore use a generated JavaScript wrapper layer that coordinates canonical wrapper lookup,
`.delete()` eviction, `[Symbol.dispose]`, and any `FinalizationRegistry` cleanup. A native-only
cache of `emscripten::val` is insufficient because it cannot observe deletion safely and is
thread-affine under pthreads.

#### 5.3 Multiple Inheritance — mitigation strategy

As established in §0.2, `embind::class_<Derived, base<Base>>` supports exactly one base. LIME
allows a `class`/`interface` to extend more than one parent (see `MultipleInheritance.lime`,
§0.2). Recommended mitigation, informed by the fact that the `.lime` fixture *already* models
explicit upcasting as ordinary static functions (`getMultiClassAsNarrow()`,
`upcastMultiInterfaceToNarrow()`):

1. Register exactly one **primary base** via embind's `base<>` — prefer the `open class` parent
   over a `narrow interface` parent when both exist, since narrow interfaces are the
   lighter-weight, more commonly-upcast-to type in this codebase.
2. For every other (secondary) parent, **flatten** its members directly onto the derived type's
   `class_<>` registration (i.e., bind `NarrowInterface::parentFunctionLight()` as
   `MultiClass::parentFunctionLight` a second time) rather than attempting a real embind
   inheritance edge.
3. For genuine polymorphic upcasts (a `MultiClass*` handed to code expecting a `NarrowInterface*`),
   rely on the LIME-level explicit conversion functions the API already exposes, and make sure the
   generator does **not** promise implicit/automatic upcasting along the secondary parent — that
   would silently misrepresent what embind can actually do.

This must be validated against `MultipleInheritanceTest`-equivalent functional tests (§8.2) before
Phase 5 is considered complete; if referential equality (§5.2) breaks under the flattening
approach, that is a hard blocker, not a follow-up item.

#### 5.4 JS → C++ callbacks and interface implementations

- For LIME `interface` types implemented on the JS side (callbacks), embind's subclassing
  mechanism (`class_<T>().allow_subclass<Wrapper>("TWrapper")`, with a C++ `wrapper<T>` trampoline
  class) is the direct analog of pybind11's `PYBIND11_OVERRIDE` trampoline pattern
  (`docs/python_pybind11_plan.md` §5.3). Unlike pybind11's GIL-acquire concern, a default
  single-threaded wasm module has no equivalent lock to manage — but see the pthreads note below.
- **Pthreads is a hard requirement, not a hypothetical**: the HERE SDK core *will* run with
  Emscripten pthreads (`-pthread` + `SharedArrayBuffer`). This makes callback re-entrancy and
  cross-thread `val` handling a first-class design concern analogous to pybind11's GIL story —
  it must be designed for up front (see §5.7), not deferred as an open question.
- For simple `LimeLambda`/callable parameters, use `emscripten::val` to hold a reference to the JS
  function and invoke it via `val::call<ReturnType>(args...)`.

#### 5.5 Exception mapping

| C++ exception | JS-visible behavior |
|---------------|----------------------|
| `std::exception` | Uncaught C++ exceptions surface as an opaque wasm abort unless `-fexceptions`/`-fwasm-exceptions` and `DISABLE_EXCEPTION_CATCHING=0` are set at compile/link time |
| Gluecodium `Return<T, Error>` failure | Generated `Error` subclass thrown as a native JS `Error` (or a generated JS class extending `Error`) |
| `std::out_of_range` | `RangeError` |
| `std::invalid_argument` | `TypeError` |

Compiling with exceptions enabled has a real wasm binary-size and performance cost (flagged in §4
of the risk table) — this is a build-flag decision, not just a generator-code decision, and belongs
in the Phase 7 CMake module alongside the `-sWASM_BIGINT` requirement.

#### 5.6 Async support (`@Async`)

Defer, same as Python's §5.5 status. Candidate approaches worth spiking later rather than now:
Emscripten **Asyncify** (works today, meaningful code-size/perf overhead) vs. the newer
**JS Promise Integration (JSPI)** proposal (lower overhead, narrower toolchain/browser support as
of this plan's writing). Do not commit to one without a dedicated spike, since this is an area
where Emscripten's recommended approach is still shifting.

---

#### 5.7 Threading: Emscripten pthreads + `SharedArrayBuffer` (hard requirement)

The HERE SDK core requires a pthreads build (`-pthread`, `PROXY_TO_PTHREAD`, and
`SharedArrayBuffer`, which in turn requires cross-origin isolation headers on the serving side).
This changes several assumptions made elsewhere in this plan:

- **Callback re-entrancy**: with `PROXY_TO_PTHREAD`, the wasm module runs on a dedicated worker,
  so JS callbacks invoked from C++ (`allow_subclass<Wrapper>` trampolines, `emscripten::val`
  lambdas) execute on that worker's thread, not the main thread. Generated trampolines must not
  assume main-thread-only execution; any DOM/UI-touching callback bodies are the *consumer's*
  responsibility to proxy (e.g. via `postMessage`), but the generator's documentation contract
  must state which thread each callback fires on.
- **Cross-thread `emscripten::val`**: `val` handles are only valid on the thread that created
  them. Any generated code that stores a `val` (e.g. a lambda held by a C++ object for later
  invocation) must either guarantee same-thread invocation or marshal through
  `emscripten_sync_run_in_main_runtime_thread`-style helpers. This is the direct analog of
  pybind11's GIL-acquire discipline and needs its own spike before Phase 5 is marked done.
- **Object identity cache (§5.2)**: the wrapper cache must be thread-safe (or per-thread) once
  multiple threads can retrieve wrappers concurrently.
- **Build flags**: `-pthread -sPTHREAD_POOL_SIZE=... -sPROXY_TO_PTHREAD=1` join `-sWASM_BIGINT=1`
  and exception flags as required link options in Phase 7; `SharedArrayBuffer` availability
  (cross-origin isolation) becomes a documented deployment requirement.
- **Functional tests (§8.2)**: the Node.js runner must enable
  `--experimental-wasm-threads` / COOP/COEP-equivalent settings as needed, and at least one test
  should exercise a callback fired from a pthread context; a browser-based pass (headless Chromium)
  covers the same under real COOP/COEP headers — both Node.js and browser are required targets
  (Q3).

Add a spike doc (`docs/js_binding_dev/spikes/pthreads_callbacks_spike/README.md`) covering cross-thread `val`
invocation and callback-from-worker behavior before committing to the Phase 5 design.

### Phase 6 — Output File Structure

Mirror `PythonNameRules.PYTHON_TARGET_DIRECTORY` / `PYBIND11_TARGET_DIRECTORY` layout:

```
<output>/js/
  <package>/<Name>.d.ts          # one .d.ts per top-level LIME type (mirrors Python's per-type .py)
  <package>/index.d.ts           # package-level re-exports
  package.json                   # npm package descriptor (parallels setup.py/pyproject.toml)
  tsconfig.json
<output>/js/embind/
  <pkg>_<Name>.cpp                # one register_<Name>(void) per top-level LIME type
  _wrapper_cache.h                # if needed per §5.2
  _module_init.cpp                # aggregates every register_* call inside one EMSCRIPTEN_BINDINGS block
```

Note one structural nuance that does **not** apply to Python: pybind11's per-type-file split
exists partly because each `.cpp` becomes an independently useful translation unit compiled into a
*dynamically loaded* extension. Under embind, every `.cpp` gets **statically linked into the same
`.wasm` binary** regardless of how many files it's split across — so the per-type split here is
purely a compile-parallelism/organization choice, not a module-boundary one (see §7,
Architecture Decision).

---

### Phase 7 — Build Integration (the largest infrastructure departure)

#### 7.1 Add `js` to the CMake-supported generator list

Mirror how `python` was wired into the CMake generator list (referenced by
`cmake/modules/gluecodium/Python.cmake` and whatever central list feeds
`gluecodium_generate(... GENERATORS cpp python ...)`).

#### 7.2 New `cmake/modules/gluecodium/Js.cmake`

Unlike `Python.cmake` (which links a normal native `.so`/`.pyd` built by the *host* compiler
against a separately-installed CPython), the entire dependency chain here must be compiled by
`em++`. This is not a drop-in analog of `gluecodium_target_python_sources()` — it needs one of:

1. **Emscripten toolchain file** applied to the whole CMake configure step
   (`-DCMAKE_TOOLCHAIN_FILE=$EMSDK/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake`),
   so the HERE SDK core, generated C++, and embind glue are all built as one `em++` invocation —
   this is the most consistent approach with the C++ generator's existing output.
2. A separate wasm-only super-build target that only pulls in the subset of the C++ core needed
   for the exposed API surface, if compiling the *entire* SDK core to wasm is not desired for size
   reasons.

Recommend spiking option 1 first (§0.3) since it requires the least new CMake machinery; only
pursue option 2 if wasm binary size becomes a demonstrated problem.

> **Spike status update (2026-08-22)**: Phase 0.3 is complete (`docs/js_binding_dev/spike_phase0_results.md`).
> The calculator example already compiles cleanly under `emcmake`/`em++` with zero source changes,
> using a *hand-written* `EMSCRIPTEN_BINDINGS` entry point. That hand-written spike is not a
> substitute for the work in §7.4 below — the point there is to replace the hand-written glue
> with generator output.

#### 7.4 Convert `examples/calculator` into a first-class JS/wasm example

**This is the right moment for the calculator JS example: immediately after Phase 7 lands, before
Phase 8 begins.** Rationale:

- It depends on everything from Phases 2–6 (generator, templates, type mapping, lifecycle
  contract, output layout) *and* on Phase 7's `Js.cmake`/toolchain wiring — attempting it earlier
  would mean hand-writing bindings again, which the Phase 0.3 spike already proved but which
  validates nothing about the generator itself.
- It is the ideal first end-to-end exercise of the generator: small enough to debug quickly, yet
  it exercises nearly every hard feature in one file — exceptions (`CalculatorException`),
  lambdas/callbacks (`SubtructCallback`), platform-implemented interfaces (`MultiplyCallback`),
  structs as parameters and return values (`DivideArguments`/`DivideResult`), C++-implemented
  interfaces returned to JS (`MinResultRetriever`), and optionals (`max`). See
  `examples/calculator/lime/Calculator.lime`.
- It directly feeds Phase 8 (use it as the first non-trivial fixture for the Node.js test runner)
  and acceptance criterion 4 (`tsc --strict` check against the generated `.d.ts`).

Concretely:

1. Add a `js` (wasm/embind) target to `examples/calculator/CMakeLists.txt`, gated behind an
   option (e.g. `-DENABLE_JS=ON`) and only meaningful when configured through `emcmake`, mirroring
   how the existing targets are gated.
2. Run Gluecodium with `-generators cpp,js` so the example consumes *generated* `.d.ts` +
   embind `.cpp` output instead of the Phase 0.3 spike's hand-written `main.cpp`.
3. Add a minimal Node.js smoke script (`node examples/calculator/js/smoke.js`) that loads the
   modularized module and exercises `summarize`, `divide`, and `min` — this doubles as the seed
   for the Phase 8 test runner.
4. Update `examples/calculator/README.md` with the emcmake build instructions.

Required `em++`/linker flags to bake into the module, all justified above:
```cmake
target_link_options(${_module_target} PRIVATE
  -lembind
  -fexceptions               # §5.5
  -sWASM_BIGINT=1            # §4.4
  -pthread                   # §5.7 — hard requirement for HERE SDK
  -sPROXY_TO_PTHREAD=1       # §5.7 — run module on a dedicated worker
  -sPTHREAD_POOL_SIZE=4      # §5.7 — sized to HERE SDK's expected concurrency; tune as needed
  -sMODULARIZE=1
  -sEXPORT_ES6=1
  -sENVIRONMENT=web,node     # Q3 — both Node.js and browser are required targets
  -sALLOW_MEMORY_GROWTH=1
)
```
Serving the output requires cross-origin isolation headers (`Cross-Origin-Opener-Policy:
same-origin`, `Cross-Origin-Embedder-Policy: require-corp`) so `SharedArrayBuffer` is available —
document this as a deployment requirement (§5.7).
```

#### 7.3 Update the generated-files list / supported-generators list

Same mechanical update `python` needed (functional-tests CMakeLists, sample-project scripts, etc.)
— enumerate exact touch points once Phase 0.3's spike build is working, since the precise list is
easiest to get right by diffing what the Python `git log` touched for the equivalent step rather
than guessing blind.

---

### Phase 8 — Testing

#### 8.1 Smoke tests — deferred until functional tests pass

**Decision: skip the smoke-test suite (and its reference files) during development; generate the
golden reference files only after all functional tests are passing.**

The existing smoke tests (`gluecodium/src/test/resources/smoke/`) compare generated output against
checked-in reference files. Every generator feature change requires regenerating those reference
files (`DUMP_ACTUAL_DIR=... ./gradlew test`), which is a tedious, error-prone, and high-churn
workflow during active development — and the JS generator will touch templates and resolvers
frequently across Phases 2–7.

Instead:
- **Functional tests are the primary correctness gate.** They compile and *execute* the generated
  code under `em++`/Node.js, which is a strictly stronger signal than textual diffing of generated
  output — a smoke test can pass while producing bindings that don't compile or run.
- **JVM-side unit tests** still cover the pure-logic pieces that functional tests can't reach
  cheaply (name resolvers, comments processing, predicates) via targeted Kotlin unit tests against
  small in-memory LIME models — but without checked-in golden files.
- **Golden reference files are generated once, at the end**: once the functional-test suite is
  fully passing (i.e., the generated bindings compile under `em++` and behave correctly in
  Node.js/browser), run `DUMP_ACTUAL_DIR=... ./gradlew test` to capture the generated output as
  the checked-in `smoke/js/` reference directory. At that point the output is known-good by
  construction, so the reference files cost one regeneration instead of dozens, and from then on
  they serve as a cheap regression tripwire for template/name-resolver changes.

This deviates from how Python was built (it inherited the full smoke suite from day one), and that
deviation is intentional: same end state, different sequencing.

#### 8.2 Functional tests

The functional-test *fixtures* (`functional-tests/functional/input/lime/*.lime`, including
`MultipleInheritance.lime`) are already shared across every generator — reuse them as-is. What's new is the **test runner**: unlike
JVM/native targets, this needs Node.js (fast inner loop, recommended first) **and** a
headless-browser pass (Playwright + Chromium) before release gating, since both environments are
required targets (Q3). Start with a `functional-tests/functional/js/` directory
using Node.js + a JS test framework (Jest, given HERE SDK's existing JS/TS tooling elsewhere, if
any — otherwise Node's built-in `node:test` is a zero-dependency option) driving the compiled
`.wasm`/`.js` module directly.

Explicitly include a `MultipleInheritance`-based functional test as a Phase 8 gating item, per
§5.3 — this is the test most likely to reveal that the flattening mitigation is incomplete.

#### 8.3 Functional test build script (conceptual)

```bash
#!/bin/bash
# Build the JS/Wasm functional tests
# 1. Run Gluecodium to generate C++ + JS/embind code
# 2. emcmake cmake + emmake make (or ninja) to produce the .wasm + glue .js
# 3. npm/node test runner exercises the compiled module
```

---

### Phase 9 — Documentation

Mirror `docs/python_pybind11_plan.md` §9:
- Update `docs/guide.md` with the JS/embind target (note: as of `python_bind`, `docs/guide.md`
  does not yet mention Python either — `grep` for "python"/"Python" in `docs/guide.md`,
  `docs/lime_attributes.md`, and `docs/external_types.md` currently returns nothing, so this is a
  pre-existing documentation gap to close for *both* targets, not something JS uniquely owes).
- Update `docs/lime_attributes.md` with the `@Js` attribute.
- Add `docs/js_binding_dev/` for phase-by-phase implementation notes, mirroring
  `docs/python_binding_dev/`.

---

### Phase 10 — Gradle Plugin Support

Defer, same status as Python's Phase 10 — revisit once Phase 7's build story is proven out, since
the Gradle plugin's job is largely to orchestrate the same CMake/toolchain invocation.

---

## 3. Implementation Order

1. Phase 0 (spikes — **hard gate**, especially 0.2 multiple inheritance and 0.3 `emcmake` build)
2. Phase 1 (model layer — low risk, mechanical, mirrors Python exactly)
3. Phase 2 (generator skeleton — structural mirror of `PythonGenerator`)
4. Phase 3 + 4 (templates + type mapping — the `Optional<T>` caster and `vector`/`map`
   registration collection are the two items likely to take longer than they look)
   — immediately followed by §4.5: a dev-only minimal build harness
   (`generate → emcmake → node`) to get an end-to-end correctness signal before Phase 5
5. Phase 5 (lifecycle/MI/callbacks — highest design risk, needs the Phase 0 spike findings;
   includes the §5.7 pthreads/cross-thread-`val` spike before the callback design is finalized)
6. Phase 6 (output structure)
7. Phase 7 (build integration — second-highest risk, do not start until Phase 0.3 spike passes)
   — immediately followed by §7.4: converting `examples/calculator` into a generated-JS example
   (the calculator JS example belongs here, not earlier: it needs the generator *and* the CMake
   wiring, and it seeds Phase 8's test runner)
8. Phase 8 (testing, in parallel with Phases 3–7 once Phase 2 lands)
9. Phase 9 (docs)
10. Phase 10 (Gradle plugin, deferred)

---

## 4. Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| No multiple inheritance in embind (`base<>` is single-parent) | **High** — blocks parity with `MultipleInheritance.lime`, which every other generator passes | Primary-base + flattened-secondary-members + explicit upcast helpers (§5.3); spike before Phase 2 |
| No automatic GC of wasm-heap objects | **High** — correctness/leak risk, and a real API-ergonomics divergence from every other target | Explicit `dispose()`/`delete()` as the documented contract; generated wrapper-layer `FinalizationRegistry` safety net enabled only where cleanup is thread-safe, and opt-in for pthread builds until marshalling is verified (§5.1, Q2) |
| Whole dependency graph must cross-compile under `em++`/Emscripten toolchain file | **High** — largest infra change of any generator added so far | Spike a minimal `emcmake` build of `examples/calculator` in Phase 0.3 before committing to Phase 7's design |
| No native `std::optional<T>` embind support | **Medium** | Hand-written value caster, spiked and documented separately (mirrors the Python chrono-caster spike) |
| `int64_t`/`uint64_t` precision loss in JS `number` | **Medium** | Require `-sWASM_BIGINT=1` unconditionally; document as an acceptance criterion, not an opt-in flag |
| Exception-handling code size/perf overhead (`-fexceptions`) | **Medium** | Accept the cost as a baseline requirement (§5.5); revisit only if binary size becomes a blocking concern |
| `@Async` story is toolchain-immature (Asyncify vs. JSPI) | **Low/Medium** | Explicitly deferred (§5.6), same posture as Python's deferred async support |
| Pthreads + `SharedArrayBuffer` required: cross-thread `val` and callback re-entrancy | **High** — HERE SDK requires a pthreads build; `val` is thread-affine and callbacks fire on the wasm worker | Design for threading up front (§5.7): spike cross-thread `val` marshalling before Phase 5; make wrapper cache thread-safe; document callback thread contract |
| Emscripten SDK version churn | **Low** | Pin an `emsdk` version for CI once Phase 0 lands |

---

## 5. List of Files to Modify/Create

### New files
- `lime-runtime/.../LimeAttributeType.kt` — add `JS` enum value (modify, not new)
- `gluecodium/src/main/resources/namerules/js.properties`
- `gluecodium/src/main/java/com/here/gluecodium/generator/js/*.kt` (see §2.1 for the full list)
- `gluecodium/src/main/resources/templates/js/*.mustache` (see §3.1)
- `cmake/modules/gluecodium/Js.cmake`
- `examples/calculator/` — add JS/wasm target + Node smoke script (§7.4; modify, not new)
- `functional-tests/functional/js/` (new test directory, mirrors `functional-tests/functional/python`
  if that exists, or the `dart`/`swift` directories otherwise)
- `docs/js_binding_dev/` (phase implementation notes, mirrors `docs/python_binding_dev/`)
- `docs/js_binding_dev/spikes/optional_caster_spike/README.md`
- `docs/js_binding_dev/spikes/mi_spike/`
- `docs/js_binding_dev/spikes/pthreads_callbacks_spike/README.md` (§5.7)

### Modified files
- `lime-loader/src/main/java/com/here/gluecodium/loader/AntlrLimeConverter.kt` (§1.2)
- `gluecodium/src/main/java/com/here/gluecodium/generator/common/GeneratorOptions.kt` (§1.4)
- `gluecodium/src/main/java/com/here/gluecodium/cli/OptionReader.kt` (§1.5)
- `gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator` (§2.3)
- `docs/guide.md`, `docs/lime_attributes.md`, `docs/external_types.md` (§9)
- `examples/calculator/CMakeLists.txt`, `examples/calculator/README.md` (§7.4)

---

## 6. Acceptance Criteria

1. All existing functional-test `.lime` fixtures generate valid embind bindings that compile under
   `em++`, **including** `MultipleInheritance.lime` with the mitigation from §5.3.
2. `-sWASM_BIGINT=1` is enforced (not optional) so `Long`/`ULong` round-trip without precision loss.
3. Referential equality (per `docs/pointer_equality.md`'s existing contract) holds for objects
   retrieved more than once from the JS side.
4. Generated `.d.ts` stubs type-check under `tsc --strict` for at least one non-trivial fixture
   (e.g., the calculator example).
5. A documented, explicit object-disposal API exists and is exercised by at least one functional
   test that verifies memory is actually released (not just that `.delete()` doesn't throw).
6. CI builds the JS target through `emcmake`/`em++` on a pinned `emsdk` version.
7. The pthreads build (`-pthread`, `PROXY_TO_PTHREAD`, `SharedArrayBuffer`) is the default
   configuration; at least one functional test exercises a callback invoked from a pthread
   context without data races or lost `val` handles (§5.7).
8. The generated module is verified in **both** Node.js and a browser (headless Chromium) —
   including the pthreads/`SharedArrayBuffer` path under real COOP/COEP headers in the browser
   case (Q3).

---

## 7. Architecture Decision: JS/TS File Organization

### Decision: one `.d.ts` per LIME type, but embind `.cpp` file granularity is a compile-time-only choice

Following Python's "one `.py` file per LIME type" decision (`docs/python_pybind11_plan.md` §7) for
the `.d.ts` side keeps parity with how consumers navigate the other four language outputs.

**Important divergence from the Python rationale**, called out explicitly so this isn't
copy-pasted without re-checking: Python's per-type `.cpp` split is partly a *loading* boundary
consideration on top of an organizational one (`PythonGenerator`'s doc comment explains each file
exposes `register_<Name>(pybind11::module_&)`, aggregated by a `_module_init.cpp`). For embind, all
`.cpp` files get **statically linked into the same `.wasm` binary regardless of file count** — so
here the same per-type split (with `register_<Name>(void)` aggregated by `_module_init.cpp`,
mirroring Python's `EMSCRIPTEN_BINDINGS` aggregation) is purely a compile-parallelism/readability
choice, not a runtime-loading one. Worth stating plainly so nobody re-derives module-boundary
reasoning that doesn't actually apply here.

---

## 8. Open Questions for Future Architecture Discussion

### Q1: Attribute name — `@Js` vs. `@Embind` vs. `@Wasm`? — RESOLVED: `@Js`

**Decision: the attribute is `@Js`.** This matches the established "attribute name = output
language" convention (`@Dart` not `@Ffi`, `@Swift` not `@Cbridge`, `@Python` not `@Pybind11`).
embind is the binding *technology*; JavaScript/TypeScript is the output *language*, and LIME
attributes name languages. It also keeps the door open to swapping the underlying technology
later (e.g. a future Emscripten binding mechanism) without breaking `.lime` files — exactly the
reasoning that makes `@Wasm` (a compilation target, not a language) and `@Embind` (a technology
that could be replaced) wrong choices. No competing convention preference exists; Phase 1 proceeds
with `JS("Js", ...)` in `LimeAttributeType.kt` as specified in §1.1.

### Q2: Object lifecycle contract — explicit-only, or `FinalizationRegistry`-assisted? — RESOLVED: explicit primary, conditional safety net

**Decision: support both mechanisms, with an explicit threading gate.** Explicit
`.delete()`/`dispose()` remains the primary, documented contract. A `FinalizationRegistry`-based
leak-reduction net is generated as part of the JavaScript wrapper layer, but it is enabled by
default only when cleanup is proven to run on the wrapper's owning WebAssembly thread:

1. **Explicit disposal (primary contract)** — every generated class exposes `.delete()` (sketched
   in the §3.3 stub template). All documentation, examples, and lint guidance present this as the
   required way to release wasm-heap objects deterministically.
2. **`FinalizationRegistry` safety net (generated, conditionally enabled)** — the generated JS
  wrapper registers each instance with a shared registry whose cleanup callback evicts generated
  cache metadata when the wrapper is GC'd. Embind's own finalization path remains responsible for
  releasing the native holder. Caveats that must be encoded in the implementation:
   - Timing is non-deterministic; never document it as a substitute for explicit disposal.
   - Cleanup callbacks must not resurrect or touch other wrappers; keep them minimal
     (pointer-freeing only).
   - Under pthreads (§5.7), the registry is opt-in until a tested marshalling mechanism exists;
     a finalizer must never call into wasm from an arbitrary JavaScript thread.
   - Provide a module-level opt-out (e.g. a config flag at module init) for embedding contexts
     where registry overhead or teardown-order issues matter, even when same-thread cleanup is
     available.
3. **Diagnostics** — expose a debug counter of live wrappers vs. deleted wrappers so tests can
   assert leak-freedom (feeds acceptance criterion 5) and users can detect missed `.delete()`
   calls in development builds.

The generated wrapper layer is also the integration point for referential-equality cache eviction
and `[Symbol.dispose]`. These lifecycle mechanisms share one canonical-wrapper ownership protocol;
they must not be implemented independently and reconciled later.

### Q3: Node.js vs. browser as the primary target environment? — RESOLVED: both are required targets

**Decision: the generated module must work in both Node.js and browsers; neither is optional.**
This constrains the Emscripten configuration as follows:

- Use `-sENVIRONMENT=web,node` so the same glue `.js` works in both runtimes.
- Keep `-sMODULARIZE=1 -sEXPORT_ES6=1` so consumers instantiate the module explicitly in either
  environment.
- Pthreads + `SharedArrayBuffer` (§5.7) is a hard requirement for both targets:
  - **Node.js**: threads work out of the box (worker support built in); use it for CI and
    functional tests since no cross-origin-isolation setup is needed.
  - **Browsers**: serving the output requires cross-origin isolation headers
    (`Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Embedder-Policy: require-corp`) for
    `SharedArrayBuffer` availability — document this as a deployment requirement, and add a
    browser smoke check (headless Chromium via Playwright or similar) to Phase 8 alongside the
    Node.js runner.
- The functional-test runner (§8.2) should treat Node.js as the fast inner loop and add a
  browser-based test pass before release gating, so browser-only issues (header misconfiguration,
  worker/COOP behavior) are caught too.

### Q4: Should the generated JS API be Promise-based even for non-`@Async` functions? — RESOLVED: no — synchronous by default

**Decision: non-`@Async` functions return plain values synchronously; only LIME-`@Async` functions
return `Promise<T>` (once §5.6 lands).** This preserves parity with every other target's behavior.

Rationale:

1. **A Promise over a blocking call is fake asynchrony.** A single-threaded wasm module blocks the
   JS event loop for the duration of any call regardless of how the result is wrapped. Under
   Option B ("wrap everything"), `await calc.divide(10, 4)` does not yield to the event loop — the
   call still runs to completion before the microtask that resolves the Promise executes. The
   consumer pays the ergonomic cost (forced `await`, harder stack traces, no synchronous access to
   results) while getting zero actual concurrency benefit.
2. **Parity across targets matters more than JS idiom here.** Teams porting logic between the
   Android/iOS/JS SDKs benefit from identical call shapes; a uniform-Promise API is a JS-only
   divergence with no compensating capability.
3. **The one real benefit of Option B** — stable signatures when a method later gains `@Async` —
   is not worth it: adding `@Async` is already a breaking signature change in every other target,
   and documenting it as such for JS is consistent.

Concretely, for `fun divide(numerator: Double, denominator: Double): DivideResult`:

```typescript
// Option A (chosen):                       // Option B (rejected):
divide(numerator: number,                   divide(numerator: number,
       denominator: number): DivideResult;         denominator: number): Promise<DivideResult>;
```

Template impact (Phase 3): the `.d.ts` templates need two return-type paths keyed on the
`@Async` predicate (`JsGeneratorPredicates`), not one uniform path; until §5.6 lands, all methods
are synchronous and the async path is simply unexercised.

### Q5: What if React Native support is wanted in the future?

React Native does **not** run bindings through Emscripten/embind. Its native-module story is
**JSI** (JavaScript Interface): C++ objects are exposed directly to the Hermes/JSC runtime via
`jsi::Object`/host classes, compiled natively per platform (no wasm, no `SharedArrayBuffer`, no
embind). Concretely, adding RN later would mean:

- **A new binding technology, but the same output language.** A hypothetical `react-native`
  target would generate JSI C++ host objects + TypeScript declarations — structurally closer to
  pybind11 than to embind (direct runtime API calls, no cross-compilation of the whole graph).
- **What can be reused from this plan**: the `@Js` LIME attribute (§1.1), the `.d.ts` template
  family (`JsStub*.mustache`), name resolvers, comments processor, and most of Phase 1's model
  layer are technology-agnostic and carry over directly.
- **What cannot be reused**: all `Embind*.mustache` templates, the Emscripten toolchain/CMake
  integration (Phase 7), pthreads/`SharedArrayBuffer` work (§5.7), and the lifecycle contract
  details (JSI host objects are GC-managed by the runtime — no `.delete()` needed, which actually
  *removes* the biggest divergence in §5.1).
- **Naming implication**: this is precisely why Q1 resolves to `@Js` and not `@Embind`/`@Wasm`.
  If the attribute were named after the technology, RN support would need a second attribute
  (`@Embind(Skip)` vs `@Jsi(...)`) on every element; with `@Js`, one attribute serves both
  targets, and any target-specific behavior is expressed through generator options, not new
  attributes.
- **Recommended posture**: do nothing now, but keep the generator's JS-facing layer
  (`.d.ts` generation, name rules, filtering) cleanly separated from the embind layer so a future
  `react-native` generator can share the former without dragging in the latter. This separation
  already exists in the §2.1 file layout (JS-facing resolvers vs. `Embind*` resolvers).

---

## Appendix: Reference Material Consulted

- `docs/python_pybind11_plan.md` — structural and reasoning template for this document.
- `docs/pointer_equality.md` — existing cross-language object-identity contract that §5.1/§5.2 build on.
- `functional-tests/functional/input/lime/MultipleInheritance.lime` — the fixture that drove the
  multiple-inheritance risk assessment in §0.2/§5.3.
- `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGenerator.kt` — closest
  existing generator to model `JsGenerator` on (no C-ABI intermediate layer, same dual-filter
  pattern).
- `cmake/modules/gluecodium/Python.cmake` — closest existing CMake integration to model
  `Js.cmake` on, with the toolchain divergence in §7 called out explicitly.
