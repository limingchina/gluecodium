# Plan: Kotlin Multiplatform (KMP) bindings for Gluecodium

Grounded against `limingchina/gluecodium` @ master (`gluecodium/src/main/java/com/here/gluecodium/generator/*` — note: files are `.kt`, the directory is still named `java` for historical reasons).

## 0. Objective

Add generation of a `commonMain` `expect` API plus `actual` implementations for
`androidMain`/`jvmMain` (JNI) and `iosMain`/`appleMain` (Kotlin/Native cinterop),
reusing the existing per-target ABI machinery instead of inventing a fourth ABI.
Non-goals for v1: JS/Wasm targets, coroutines/Flow surface (layer on top of the
existing `@Async` callback model later), desktop/linux native targets (should
fall out "for free" once appleMain works, since they'd reuse the same cbridge
C ABI, just a different cinterop target triple).

## 1. What's actually there (corrections from my first pass)

`generator/` has 9 subpackages, but only **5 are registered generators**. Registration
is `ServiceLoader`-based — `Generator` is an SPI interface, and the whole list lives in
one file:

```
gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator
  com.here.gluecodium.generator.cpp.CppGenerator
  com.here.gluecodium.generator.java.JavaGenerator
  com.here.gluecodium.generator.swift.SwiftGenerator
  com.here.gluecodium.generator.dart.DartGenerator
  com.here.gluecodium.generator.kotlin.KotlinGenerator
```

`cbridge`, `jni`, `ffi`, `common` are **not** generators in their own right — they're
internal helper packages consumed by one or more of the five real generators. This
matters because it tells you exactly where a KMP generator would plug in (a 6th
`ServiceLoader` entry) and which internal packages it can reuse.

**Correction #1 — there's already a standalone `KotlinGenerator`, and it's not a
wrapper around `JavaGenerator`.** I'd assumed an "android"/"android-kotlin" split
from a stale CHANGELOG read. What's actually true: `JavaGenerator` and
`KotlinGenerator` are sibling generators that each independently import
`com.here.gluecodium.generator.jni.JniTemplates`, `CppNameCache`, `CppNameRules`.
Both emit their own idiomatic surface (Java classes / Kotlin classes) over the
**same shared JNI-glue templates**, so the native method signatures line up and
one native `.so` serves either. That's almost certainly what
`GLUECODIUM_FORCE_USAGE_OF_JNI_FROM_JAVA_GENERATOR` is for — dedup the generated
JNI C++ glue when both `java` and `kotlin` generators run in the same build.

Practical consequence for the plan: the JVM/Android `actual` generator should be
a **third sibling consumer of `JniTemplates`** (new Kotlin templates emitting
`actual class ... external fun ...`), not a retrofit of `KotlinGenerator`'s
existing (non-expect/actual-aware) output. Structurally simpler than what I
originally proposed, and follows an established pattern instead of a novel one.

**Correction #2 — there are *two* C-ABI generators, not one, and they're not
interchangeable.**

| | `cbridge` | `ffi` |
|---|---|---|
| Consumed by | `SwiftGenerator` only | `DartGenerator` only |
| Registered as own generator? | No — `internal class CBridgeGenerator`, instantiated directly inside `SwiftGenerator` | Same pattern, inside `DartGenerator` |
| Header shape | `extern "C" { ... }`, opaque `_baseRef` handles, `CBridgeClassHeader.mustache` etc. | `extern "C" { ... }`, opaque handles via `OpaqueHandle.h`, `#include "dart_api_dl.h"` |
| Callback/async mechanism | Plain C function-pointer struct: `{ void* context; void(*release)(void*); ReturnType(*call)(void*, ...); }` (confirmed in `CBridgeLambdaHeader.mustache`) — synchronous, no runtime-specific plumbing | Built on `dart_api_dl.h` — Dart's isolate message-posting C API, needed because dart:ffi callbacks from arbitrary native threads must cross into a Dart isolate via `Dart_PostCObject`-style machinery |
| Object identity | `CachedProxyBase.h` / `WrapperCacheImpl.mustache` | `FfiProxyCacheImpl.mustache` / `FfiInstanceCacheImpl.mustache` |

Both are legitimate plain-C headers a `cinterop` `.def` file could point at. But
`ffi`'s callback path is baked around Dart's isolate model, which Kotlin/Native
has no equivalent requirement for — a native thread can call a Kotlin/Native
callback directly (subject to the memory-manager/thread rules in §4.3, but no
message-posting indirection needed). **`cbridge`'s plain function-pointer-struct
callback ABI is the closer match and the one to build on.** This also answers
the "does this interact with the Dart-drop evaluation (E2)" question directly:
it doesn't — a KMP-native generator would depend on `cbridge`, and dropping
`ffi`/`DartGenerator` has no bearing on it.

**Correction #3 — options are not per-generator classes.** There's one shared
`GeneratorOptions` data class (`generator/common/GeneratorOptions.kt`) with
per-language fields bolted on as the languages were added: `javaPackages`,
`kotlinPackages`, `kotlinInternalPackages`, `swiftExposeInternals`,
`dartDisableFinalizableMarker`, plus shared `cppRootNamespace`/`cppInternalNamespace`,
and a `Configuration` per language loaded from `namerules/<lang>.properties`
(`kotlinNameRules` from `namerules/kotlin.properties` already exists). A KMP
generator should follow the same convention — new fields on `GeneratorOptions`
(e.g. `kmpPackages`, `kmpNativeTargets`) — not a bespoke `KmpGeneratorOptions`
type as I originally sketched.

**Correction #4 — `CBridgeGenerator` visibility is not a blocker, but its
*invocation* is currently exclusive to Swift.** It's `internal`, which in Kotlin
is module-scoped, not package-scoped — new code added inside the same
`gluecodium` Gradle module can use it freely, no visibility change needed. The
real design decision is: `SwiftGenerator` currently constructs its own
`CBridgeGenerator` instance and owns its output. If a new KMP-native generator
also runs in the same invocation and also wants CBridge's C header/impl, you
either (a) let both generators independently instantiate `CBridgeGenerator` and
rely on `SplitSourceSetCache`/collision checking (`Gluecodium.checkForFileNameCollisions`)
to dedupe identical output, or (b) refactor so CBridge generation happens once,
upstream of both consumers, and is passed in. (a) is far less invasive and
matches how the cache is already structured to tolerate this — worth spiking
before assuming (b) is necessary.

## 2. Reuse map (revised)

| KMP source set | ABI | Reuses |
|---|---|---|
| `commonMain` | none — pure `expect` decls | `KotlinNameRules`/`namerules/kotlin.properties` (so public names match existing `KotlinGenerator` output exactly), LIME model walk shared with `KotlinGenerator` |
| `androidMain`/`jvmMain` | JNI | `generator/jni/JniTemplates`, `CppNameCache`, `CppNameRules` — same three things `JavaGenerator` and `KotlinGenerator` already both import. New: Kotlin `actual`-flavored templates only. |
| `iosMain`/`appleMain` | `cbridge` C ABI | `CBridgeGenerator`, `CBridgeNameResolver`, its proxy-cache and function-pointer-table callback convention — same things `SwiftGenerator` already imports. New: Kotlin/Native idiomatic templates + a `cinterop` `.def` file + a klib-generation build step. |

## 3. New components

```
generator/kmp/
  common/
    KmpCommonGenerator.kt      # new 6th ServiceLoader entry (shortName "kmp-common" or similar)
    templates/*.mustache       # expect class/interface/fun, reusing KotlinNameRules
  jvmActual/
    KmpJvmActualGenerator.kt   # sibling of JavaGenerator/KotlinGenerator; imports JniTemplates directly
    templates/*.mustache
  nativeActual/
    KmpNativeActualGenerator.kt   # imports CBridgeGenerator/CBridgeNameResolver directly, like SwiftGenerator does
    templates/*.mustache          # idiomatic Kotlin/Native over cinterop-generated raw bindings
```

Each is a `Generator` SPI implementation registered in
`META-INF/services/com.here.gluecodium.generator.common.Generator`, invoked via
`-generators kmp-common,kmp-jvm,kmp-native` (independent invocations, same as
`java`/`kotlin`/`swift` today — lets each source set be generated/tested
independently in CI).

`GeneratorOptions` gets new fields (`kmpPackages`, `kmpInternalPackages`, a
`kmpNameRules` `Configuration` off a new `namerules/kmp.properties`, possibly
`kmpNativeTargets: List<String>` for which Kotlin/Native targets to emit
`cinterop` `.def` scaffolding for).

## 4. Design notes per source set

### 4.1 `commonMain`

Walk the same LIME model `KotlinGenerator` walks; stop at signature level,
emit `expect class`/`expect interface`/`expect fun`, no bodies. Reuse
`KotlinNameRules` so the emitted public names are byte-for-byte what
`KotlinGenerator` already produces — this is what makes §4.2 close to
mechanical. `LimeOverloadsValidator` (already imported by `KotlinGenerator`)
should be reusable as-is for validating the common-side overload set, since
Kotlin's own overload rules apply the same way to `expect` declarations.

Watch item: `expect`/`actual` requires *exact* signature match after each
side's own type-mapping. Anywhere `KotlinGenerator`'s `KotlinValueResolver` or
`KotlinSignatureResolver` currently make target-specific decisions (default
values, nullable-boxing) that a Kotlin/Native actual might resolve differently
against `cbridge` types, the two sides can silently diverge and fail to
type-check as `actual`. Needs a dedicated conformance check, not an assumption.

### 4.2 `androidMain` actual

New templates only — reuse `JniTemplates`/`CppNameCache`/`CppNameRules`
directly, same three imports `JavaGenerator` and `KotlinGenerator` already
share. Lowest-risk piece of the whole plan: same ABI, same JNI glue, just a
third template set emitting `actual` + expect-conformant signatures instead of
a freestanding class.

### 4.3 `iosMain`/`appleMain` actual

Two-stage build, not a single Gluecodium invocation:

1. `CBridgeGenerator` emits the C header/impl (as it already does for Swift
   builds) — see §1 Correction #4 for the collision-handling question this raises
   if `swift` and `kmp-native` run in the same invocation.
2. A `cinterop` `.def` file (generated by Gluecodium, or hand-maintained
   initially — worth prototyping both) points `cinterop` at that header,
   producing a klib with raw `CPointer`/`COpaquePointer`/`CFunction<...>`
   bindings. The function-pointer-struct callback convention confirmed in
   `CBridgeLambdaHeader.mustache` maps cleanly onto cinterop's struct-of-function-pointers
   support — no isolate/message-posting layer needed (contrast with `ffi`, see §1).
3. `KmpNativeActualGenerator` emits a thin idiomatic-Kotlin `actual` layer over
   the raw cinterop bindings — the same job `SwiftGenerator` does over
   `CBridgeGenerator` output, targeting Kotlin/Native syntax and cinterop's
   calling convention instead of Swift's.

Object identity: reuse `cbridge`'s existing proxy/wrapper cache
(`CachedProxyBase.h`/`WrapperCacheImpl.mustache`) rather than building a second
cache on the Kotlin/Native side — otherwise Swift and Kotlin/Native consumers
of the same underlying C++ object could observe different identities, a real
regression versus what `cbridge` already guarantees today.

Memory/lifetime: JNI's generated finalization assumes JVM GC semantics.
Kotlin/Native's memory manager uses `Cleaner`/`createCleaner`, not finalizers,
and has its own threading rules. Given the `libheresdk.so`
`pthread_mutex_lock`-on-destroyed-mutex teardown race and the
`__clang_call_terminate` destructor-exception crash already chased down on the
JNI/Swift sides respectively, native-actual teardown ordering deserves its own
test pass rather than an assumed port of either existing finalizer pattern.

## 5. Build orchestration

JNI-based output is pure Kotlin source — no build step needed before `kotlinc`
compiles it. `cinterop` output is not: it needs the C header available and
`cinterop` run as a distinct Gradle task producing a klib *before* Kotlin
compilation of anything that imports it. The existing `gluecodium-gradle`
plugin is JVM/Android-oriented and almost certainly doesn't model this
dependency edge today (worth confirming by reading it directly — not yet
checked in this pass). Needed: `generateCBridgeHeaders` → `cinterop` (per
native target) → `KmpNativeActualGenerator` output → compile, as an explicit
task graph, plus the CMake-side dedup question from §1 Correction #4 if
`swift` and `kmp-native` coexist in one build.

## 6. Phased delivery

1. **Spike**: confirm the collision-handling assumption in §1 Correction #4
   (run `swift` + a stub `kmp-native` generator that also instantiates
   `CBridgeGenerator` in the same invocation, check `SplitSourceSetCache`/
   `checkForFileNameCollisions` behavior) — this determines whether §4.3 needs
   a refactor before any template work starts, or not.
2. **`commonMain` expect generator** on a small IDL subset (structs + simple
   interfaces, no generics/collections) — validate expect/actual signature
   equality against a hand-written JVM actual before generating either actual
   automatically.
3. **`androidMain` actual** — new `JniTemplates`-based templates; get a
   JVM-only KMP module compiling and passing existing Android functional
   tests.
4. **`iosMain` actual** via `cbridge` + `cinterop` — structs/enums first (no
   proxy cache needed), then interfaces/classes (proxy cache + lifetime).
5. **Build glue** (§5) + CI.
6. **Coverage pass**: generics, collections, `@Async`/callbacks, bring `kmp`
   generator parity with what `kotlin`/`swift` already support.

## 7. Open questions

- **Q1**: Does `gluecodium-gradle` already have any task-graph precedent for a
  multi-stage generate → external-tool → generate pipeline (haven't read it
  yet), or is the `cinterop` ordering genuinely new territory for this repo's
  build tooling?
- **Q2**: For §1 Correction #4 — is (a) (let both generators instantiate
  `CBridgeGenerator`, rely on collision detection) actually safe, or does
  `CBridgeGenerator`'s constructor have side effects (e.g. `CppNameCache`
  mutation) that make two instances in one process unsafe even if the *output*
  would collide-and-dedupe correctly?
- **Q3**: Target scope for v1 — Android + iOS only, or does parity with any
  existing desktop HERE SDK target matter for the first cut?

## 8. Relative complexity ranking

1. `androidMain` actual — low (new templates over an already-shared ABI)
2. `commonMain` expect — low/medium (mechanical once `KotlinNameRules` reuse is confirmed)
3. Build orchestration (§5) — medium, possibly higher depending on Q1
4. `iosMain` actual (structs/enums) — medium
5. `iosMain` actual (interfaces/classes, proxy cache, lifetime) — high — the
   JNI-teardown class of bug has a native-memory-manager analog here, plus
   whatever the answer to Q2 turns out to be
