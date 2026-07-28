# Plan: Add Kotlin Multiplatform (KMP) Binding Support to Gluecodium

*Grounded against `limingchina/gluecodium` @ master (`gluecodium/src/main/java/com/here/gluecodium/generator/*` — note: files are `.kt`, the directory is still named `java` for historical reasons).*

## 1. Overview

**Objective:** Add generation of a `commonMain` `expect` API plus `actual` implementations for `androidMain`/`jvmMain` (JNI) and `iosMain`/`appleMain` (Kotlin/Native `cinterop`), reusing the existing per-target ABI machinery instead of inventing a fourth ABI.

**Current State:** Gluecodium generates platform-specific bindings:
- **Android:** Kotlin/Java bindings using JNI.
- **iOS:** Swift bindings (interacting with C++ via a pure-C CBridge layer).
- **Flutter:** Dart bindings via FFI.

**Target State:** Three new generators (registered as `ServiceLoader` entries) that produce:
1. `commonMain`: Kotlin `expect` declarations (interfaces, classes, structs, enums).
2. `androidMain`/`jvmMain`: `actual` implementations using JNI (bridging to existing C++).
3. `iosMain`/`appleMain`: `actual` implementations that reuse the existing **CBridge C ABI** layer via Kotlin/Native `cinterop`, eliminating the need for Swift or Objective-C interop.

**Non-goals for v1:** JS/Wasm targets, coroutines/Flow surface (layer on top of the existing `@Async` callback model later), desktop/linux native targets (should fall out "for free" once `appleMain` works, since they'd reuse the same CBridge C ABI, just a different `cinterop` target triple).

---

## 2. Codebase Ground Truth

Before detailing the plan, here are the key architectural facts discovered by reading the actual Gluecodium source. These correct several assumptions from earlier drafts.

### 2.1. Five Registered Generators (Not Nine)

`generator/` has 9 subpackages, but only **5 are registered generators**. Registration is `ServiceLoader`-based — `Generator` is an SPI interface, and the whole list lives in one file:

```
gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator
  com.here.gluecodium.generator.cpp.CppGenerator
  com.here.gluecodium.generator.java.JavaGenerator
  com.here.gluecodium.generator.swift.SwiftGenerator
  com.here.gluecodium.generator.dart.DartGenerator
  com.here.gluecodium.generator.kotlin.KotlinGenerator
```

`cbridge`, `jni`, `ffi`, `common` are **not** generators in their own right — they're internal helper packages consumed by one or more of the five real generators. This tells us exactly where a KMP generator plugs in (additional `ServiceLoader` entries) and which internal packages it can reuse.

### 2.2. `JavaGenerator` and `KotlinGenerator` Are Siblings (Not Wrapper/Wrapped)

There's already a standalone `KotlinGenerator`, and it's **not a wrapper around `JavaGenerator`**. What's actually true: `JavaGenerator` and `KotlinGenerator` are sibling generators that each independently import `com.here.gluecodium.generator.jni.JniTemplates`, `CppNameCache`, `CppNameRules`. Both emit their own idiomatic surface (Java classes / Kotlin classes) over the **same shared JNI-glue templates**, so the native method signatures line up and one native `.so` serves either. That's almost certainly what `GLUECODIUM_FORCE_USAGE_OF_JNI_FROM_JAVA_GENERATOR` is for — dedup the generated JNI C++ glue when both `java` and `kotlin` generators run in the same build.

**Consequence:** The JVM/Android `actual` generator should be a **third sibling consumer of `JniTemplates`** (new Kotlin templates emitting `actual class ... external fun ...`), not a retrofit of `KotlinGenerator`'s existing (non-expect/actual-aware) output. Structurally simpler than retrofitting, and follows an established pattern.

### 2.3. Two C-ABI Generators: `cbridge` vs `ffi` (Not Interchangeable)

| | `cbridge` | `ffi` |
|---|---|---|
| Consumed by | `SwiftGenerator` only | `DartGenerator` only |
| Registered as own generator? | No — `internal class CBridgeGenerator`, instantiated directly inside `SwiftGenerator` | Same pattern, inside `DartGenerator` |
| Header shape | `extern "C" { ... }`, opaque `_baseRef` handles, `CBridgeClassHeader.mustache` etc. | `extern "C" { ... }`, opaque handles via `OpaqueHandle.h`, `#include "dart_api_dl.h"` |
| Callback/async mechanism | Plain C function-pointer struct: `{ void* context; void(*release)(void*); ReturnType(*call)(void*, ...); }` (confirmed in `CBridgeLambdaHeader.mustache`) — synchronous, no runtime-specific plumbing | Built on `dart_api_dl.h` — Dart's isolate message-posting C API, needed because `dart:ffi` callbacks from arbitrary native threads must cross into a Dart isolate via `Dart_PostCObject`-style machinery |
| Object identity | `CachedProxyBase.h` / `WrapperCacheImpl.mustache` | `FfiProxyCacheImpl.mustache` / `FfiInstanceCacheImpl.mustache` |

Both are legitimate plain-C headers a `cinterop` `.def` file could point at. But `ffi`'s callback path is baked around Dart's isolate model, which Kotlin/Native has no equivalent requirement for — a native thread can call a Kotlin/Native callback directly (subject to memory-manager/thread rules, but no message-posting indirection needed). **`cbridge`'s plain function-pointer-struct callback ABI is the closer match and the one to build on.** This also means a KMP-native generator would depend on `cbridge`, and dropping `ffi`/`DartGenerator` has no bearing on it.

### 2.4. Options Are Not Per-Generator Classes

There's one shared `GeneratorOptions` data class (`generator/common/GeneratorOptions.kt`) with per-language fields bolted on as languages were added: `javaPackages`, `kotlinPackages`, `kotlinInternalPackages`, `swiftExposeInternals`, `dartDisableFinalizableMarker`, plus shared `cppRootNamespace`/`cppInternalNamespace`, and a `Configuration` per language loaded from `namerules/<lang>.properties` (`kotlinNameRules` from `namerules/kotlin.properties` already exists). A KMP generator should follow the same convention — new fields on `GeneratorOptions` (e.g. `kmpPackages`, `kmpNativeTargets`) — not a bespoke `KmpGeneratorOptions` type.

### 2.5. `CBridgeGenerator` Visibility Is Not a Blocker

`CBridgeGenerator` is `internal`, which in Kotlin is module-scoped (not package-scoped) — new code added inside the same `gluecodium` Gradle module can use it freely, no visibility change needed. The real design decision is: `SwiftGenerator` currently constructs its own `CBridgeGenerator` instance and owns its output. If a new KMP-native generator also runs in the same invocation and also wants CBridge's C header/impl, you either:

- **(a)** Let both generators independently instantiate `CBridgeGenerator` and rely on `SplitSourceSetCache`/collision checking (`Gluecodium.checkForFileNameCollisions`) to dedupe identical output, or
- **(b)** Refactor so CBridge generation happens once, upstream of both consumers, and is passed in.

Option (a) is far less invasive and matches how the cache is already structured to tolerate this — worth spiking before assuming (b) is necessary. See §7 (Open Questions, Q2).

---

## 3. Architecture & Design Strategy

KMP support requires a shift from "generate a class" to "generate an `expect` declaration and `actual` implementations across source sets."

### 3.1. The "Expect/Actual" Pattern

Gluecodium will generate three distinct source sets via three independent generators:

1. **Common Source (`commonMain`):**
   - Generates `expect class`/`expect interface`/`expect fun` declarations — no bodies.
   - Structs generate as `data class` (standard KMP supports these without expect/actual).
   - Enums generate as `enum class`.
   - Contains no C++ interop logic.
2. **Android Source (`androidMain`/`jvmMain`):**
   - Generates `actual class` implementations.
   - Wraps the existing JNI C++ bridge code via `JniTemplates` (same as `JavaGenerator`/`KotlinGenerator`).
   - Uses the existing `JniReference` handling logic.
3. **iOS Source (`iosMain`/`appleMain`):**
   - Generates `actual class` implementations.
   - Reuses the existing **CBridge C ABI** (pure C `extern "C"` functions with `_baseRef` opaque handles) as the interop target via Kotlin/Native `cinterop`.
   - Generates `cinterop` `.def` definition files pointing at the existing `cbridge/include/*.h` headers.
   - Generates Kotlin wrappers that call the CBridge C functions and manage handle lifetimes in Kotlin.

### 3.2. Current iOS Binding Architecture

Gluecodium's existing iOS binding stack has three layers:

```
┌─────────────────────────────────────────┐
│  Swift API (SwiftClassDefinition)       │  ← Public Swift classes/enums/structs
│  - Public interface for app developers  │
├─────────────────────────────────────────┤
│  Swift Conversion (SwiftClassConversion) │  ← getRef / copyFromCType / moveToCType
│  - Handle ↔ Swift object bridging        │    + wrapper cache + type repository
├─────────────────────────────────────────┤
│  CBridge (C wrapper, extern "C")         │  ← _baseRef handles, release/copy, etc.
│  - Pure C headers + Objective-C++ impl   │    Compiled into the framework binary
├─────────────────────────────────────────┤
│  C++ Core (abstract classes)             │  ← The actual SDK logic
└─────────────────────────────────────────┘
```

Key observations:
- The **CBridge layer is pure C ABI** (`extern "C"`, `_baseRef` = opaque handle = `void*`), not Objective-C. See `CBridgeHeader.mustache` and `CBridgeClassHeader.mustache`.
- The **Swift conversion layer** (`SwiftClassConversion.mustache`) handles handle↔object translation, wrapper caching, and type dispatch — all of which have direct Kotlin equivalents.
- The **Dart generator** already follows a similar pattern: generating C wrappers (`ffi/*.h`) + Dart wrappers that call through `dart:ffi`. However, `ffi`'s callback mechanism is Dart-isolate-specific (see §2.3), making `cbridge` the better reuse target for KMP.

### 3.3. KMP iOS Architecture: CBridge-cinterop Reuse

The KMP `iosMain` reuses the CBridge C ABI layer and replaces the Swift conversion layer with a Kotlin equivalent:

```
┌──────────────────────────────────────────────────┐
│              EXISTING iOS FRAMEWORK              │
│  ┌─────────────┐  ┌──────────┐  ┌────────────┐  │
│  │  C++ Core   │  │  CBridge │  │   Swift    │  │
│  │  (logic)    │←──│  (C ABI) │←──│  (API)     │  │
│  └─────────────┘  └────┬─────┘  └────────────┘  │
│                        │  (optional, for        │
│                        │   non-KMP customers)    │
└────────────────────────┼─────────────────────────┘
                         │
                    cinterop .def
                         │
┌────────────────────────┼─────────────────────────┐
│              KMP iosMain                         │
│  ┌─────────────────────┴───────────────────────┐ │
│  │  Kotlin/Native actual class                 │ │
│  │  - Calls CBridge C functions via cinterop   │ │
│  │  - Manages _baseRef handles in Kotlin       │ │
│  │  - Implements expect declarations           │ │
│  │  - Kotlin wrapper cache (MutableMap)        │ │
│  │  - Kotlin type repository (Map<String, Fn>) │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Why reuse CBridge instead of `ffi`, Swift, or Objective-C:**

| Aspect | CBridge C ABI (Recommended) | `ffi` (Dart) | Objective-C | Swift |
|---|---|---|---|---|
| Kotlin/Native interop | ✅ `cinterop` (native support) | ⚠️ Works but callback ABI is Dart-specific | ⚠️ Works but more complex (ARC, blocks) | ❌ Not supported |
| Already in framework | ✅ Compiled into existing `.framework` | ❌ Separate, Dart-specific | ❌ Would need new generation | ❌ Cannot call from Kotlin |
| Callback mechanism | ✅ Plain function-pointer struct (synchronous) | ❌ Dart isolate message-posting (`dart_api_dl.h`) | ⚠️ ARC/block complexity | ❌ N/A |
| Maturity | ✅ Battle-tested in production | ✅ Production (Dart-only) | ❌ Gluecodium doesn't generate Obj-C | ❌ N/A |
| Memory management | ✅ Explicit handle ref/unref | ⚠️ Dart finalizer-specific | ⚠️ ARC interaction complexity | ❌ N/A |

### 3.4. Reuse Map

| KMP source set | ABI | Reuses |
|---|---|---|
| `commonMain` | none — pure `expect` decls | `KotlinNameRules`/`namerules/kotlin.properties` (so public names match existing `KotlinGenerator` output exactly), LIME model walk shared with `KotlinGenerator` |
| `androidMain`/`jvmMain` | JNI | `generator/jni/JniTemplates`, `CppNameCache`, `CppNameRules` — same three things `JavaGenerator` and `KotlinGenerator` already both import. New: Kotlin `actual`-flavored templates only. |
| `iosMain`/`appleMain` | `cbridge` C ABI | `CBridgeGenerator`, `CBridgeNameResolver`, its proxy-cache and function-pointer-table callback convention — same things `SwiftGenerator` already imports. New: Kotlin/Native idiomatic templates + a `cinterop` `.def` file + a klib-generation build step. |

### 3.5. Directory Structure Output

The output directory will follow the standard KMP `sourceSets` structure:

```text
output/
└── kotlin-multiplatform/
    ├── build.gradle.kts           (Optional: Template build file)
    ├── cinterop/                  (Generated cinterop definition files)
    │   └── com_example_sdk.def    (One .def per package/module)
    └── src/
        ├── commonMain/kotlin/com/example/...
        ├── androidMain/kotlin/com/example/...
        └── iosMain/kotlin/com/example/...
```

---

## 4. New Components

```
generator/kmp/
  common/
    KmpCommonGenerator.kt      # new ServiceLoader entry (shortName "kmp-common")
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

---

## 5. Design Notes Per Source Set

### 5.1. `commonMain`

Walk the same LIME model `KotlinGenerator` walks; stop at signature level, emit `expect class`/`expect interface`/`expect fun`, no bodies. Reuse `KotlinNameRules` so the emitted public names are byte-for-byte what `KotlinGenerator` already produces — this is what makes the `androidMain` actual close to mechanical. `LimeOverloadsValidator` (already imported by `KotlinGenerator`) should be reusable as-is for validating the common-side overload set, since Kotlin's own overload rules apply the same way to `expect` declarations.

**Watch item:** `expect`/`actual` requires *exact* signature match after each side's own type-mapping. Anywhere `KotlinGenerator`'s `KotlinValueResolver` or `KotlinSignatureResolver` currently make target-specific decisions (default values, nullable-boxing) that a Kotlin/Native actual might resolve differently against `cbridge` types, the two sides can silently diverge and fail to type-check as `actual`. Needs a dedicated conformance check, not an assumption.

**Type Mapping:**
- Ensure the type mapper uses Kotlin common types (e.g., `String`, `List`, `Map`) instead of platform-specific types like `java.util.List` or Android-specific `Context`.

### 5.2. `androidMain`/`jvmMain` Actual

New templates only — reuse `JniTemplates`/`CppNameCache`/`CppNameRules` directly, same three imports `JavaGenerator` and `KotlinGenerator` already share. Lowest-risk piece of the whole plan: same ABI, same JNI glue, just a third template set emitting `actual` + expect-conformant signatures instead of a freestanding class.

**Template pattern:**
```kotlin
actual class MyClass private constructor(private val nativeHandle: Long) {
    actual fun doSomething(param: String): Int {
        return nativeDoSomething(nativeHandle, param)
    }
    private external fun nativeDoSomething(handle: Long, param: String): Int
    companion object {
        init { System.loadLibrary("heresdk") }
        actual fun create(): MyClass = MyClass(nativeCreate())
        private external fun nativeCreate(): Long
    }
}
```

Reuse the existing C++ JNI generation logic (the `.cpp` files). The `.kt` files must now bind to the native library via `System.loadLibrary` within the actual class scope.

### 5.3. `iosMain`/`appleMain` Actual

Two-stage build, not a single Gluecodium invocation:

1. `CBridgeGenerator` emits the C header/impl (as it already does for Swift builds) — see §2.5 for the collision-handling question this raises if `swift` and `kmp-native` run in the same invocation.

2. A `cinterop` `.def` file (generated by Gluecodium, or hand-maintained initially — worth prototyping both) points `cinterop` at that header, producing a klib with raw `CPointer`/`COpaquePointer`/`CFunction<...>` bindings. The function-pointer-struct callback convention confirmed in `CBridgeLambdaHeader.mustache` maps cleanly onto cinterop's struct-of-function-pointers support — no isolate/message-posting layer needed (contrast with `ffi`, see §2.3).

3. `KmpNativeActualGenerator` emits a thin idiomatic-Kotlin `actual` layer over the raw cinterop bindings — the same job `SwiftGenerator` does over `CBridgeGenerator` output, targeting Kotlin/Native syntax and cinterop's calling convention instead of Swift's.

**`cinterop` Definition Files:**

For each LIME package/module, generate a `.def` file:
```def
// com_example_sdk.def
language = C
headers = cbridge/include/MyClass.h cbridge/include/MyStruct.h ...
package = com.example.sdk.cbridge
linkerOpts = -lheresdk
```

This makes all CBridge C functions available to Kotlin/Native as Kotlin functions via `kotlinx.cinterop`.

**Generated `iosMain` Kotlin Actual Classes:**

The generated Kotlin classes mirror the Swift conversion logic (`SwiftClassConversion.mustache`) but in Kotlin/Native idioms:

```kotlin
// iosMain actual implementation
actual class MyClass private constructor(private val handle: _baseRef) : NativeBase {

    actual fun doSomething(param: String): Int {
        val cParam = moveToCType(param)  // Returns StringHandle
        val result = cbridge.MyClass_doSomething(handle, cParam.ref)
        cParam.release()
        return result
    }

    actual companion object {
        actual fun create(): MyClass {
            val handle = cbridge.MyClass_create()
            guard handle != 0L else { throw IllegalStateException("Nullptr") }
            return MyClass(handle).also { wrapperCache[handle] = it }
        }
    }

    override val c_handle: _baseRef get() = handle

    protected fun finalize() {
        cbridge.MyClass_release_handle(handle)
    }
}
```

**Kotlin Conversion Functions:**

Port the Swift conversion layer to Kotlin. These are the Kotlin equivalents of `SwiftClassConversion.mustache`:

| Swift Function | Kotlin Equivalent | Purpose |
|---|---|---|
| `copyFromCType(_ handle: _baseRef) -> MyClass` | `fun copyFromCType(handle: _baseRef): MyClass` | Construct wrapper from handle (non-owning) |
| `moveFromCType(_ handle: _baseRef) -> MyClass` | `fun moveFromCType(handle: _baseRef): MyClass` | Construct wrapper from handle (owning, releases on GC) |
| `copyToCType(_ swiftClass: MyClass) -> RefHolder` | `fun copyToCType(obj: MyClass): RefHolder` | Extract handle from wrapper (non-owning copy) |
| `moveToCType(_ swiftClass: MyClass) -> RefHolder` | `fun moveToCType(obj: MyClass): RefHolder` | Extract handle from wrapper (owning move) |
| `_CBridgeInitMyClass(handle:)` | `fun cbBridgeInit(handle: _baseRef): Any` | Type-repository dispatch for interface proxies |

**Object Identity:**

Reuse `cbridge`'s existing proxy/wrapper cache (`CachedProxyBase.h`/`WrapperCacheImpl.mustache`) rather than building a second cache on the Kotlin/Native side — otherwise Swift and Kotlin/Native consumers of the same underlying C++ object could observe different identities, a real regression versus what `cbridge` already guarantees today.

**Wrapper Cache & Type Repository (Kotlin side):**

```kotlin
// Wrapper cache: maps C++ pointer → Kotlin wrapper (prevents duplicate wrappers)
private val wrapperCache = mutableMapOf<_baseRef, MyClass>()

// Type repository: maps type-id string → constructor function (for interface proxies)
private val typeRepository = mutableMapOf<String, (_baseRef) -> Any>()
```

Sync with the C++ cache via the existing `_get_swift_object_from_wrapper_cache` / `_cache_swift_object_wrapper` C functions.

**Memory/Lifetime:**

JNI's generated finalization assumes JVM GC semantics. Kotlin/Native's memory manager uses `Cleaner`/`createCleaner`, not finalizers, and has its own threading rules. Given the `libheresdk.so` `pthread_mutex_lock`-on-destroyed-mutex teardown race and the `__clang_call_terminate` destructor-exception crash already chased down on the JNI/Swift sides respectively, native-actual teardown ordering deserves its own test pass rather than an assumed port of either existing finalizer pattern.

Key considerations:
- Use Kotlin `Cleaner` (or `finalize()`) to call `MyClass_release_handle()` when the Kotlin wrapper is collected.
- For non-owning references (copied handles), do not release — the original owner holds the reference.
- For interface proxies (C++ → Kotlin callbacks), use the existing `CachedProxyBase` mechanism via CBridge.

---

## 6. Build Orchestration

JNI-based output is pure Kotlin source — no build step needed before `kotlinc` compiles it. `cinterop` output is not: it needs the C header available and `cinterop` run as a distinct Gradle task producing a klib *before* Kotlin compilation of anything that imports it. The existing `gluecodium-gradle` plugin is JVM/Android-oriented and almost certainly doesn't model this dependency edge today (worth confirming by reading it directly — see Open Question Q1). 

Needed task graph:
```
generateCBridgeHeaders → cinterop (per native target) → KmpNativeActualGenerator output → compile
```

Plus the CMake-side dedup question from §2.5 if `swift` and `kmp-native` coexist in one build.

**Gradle Plugin Configuration:**

Generate a boilerplate `build.gradle.kts` file configured for Multiplatform:

```kotlin
kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        val commonMain by getting { ... }
        val androidMain by getting { ... }
        val iosMain by creating {
            dependencies {
                // cinterop-generated bindings
            }
        }
        val iosX64Main by getting { dependsOn(iosMain) }
        val iosArm64Main by getting { dependsOn(iosMain) }
        val iosSimulatorArm64Main by getting { dependsOn(iosMain) }
    }

    // cinterop configuration for CBridge headers
    cocoapods {
        // or framework dependency
    }
}
```

**Framework Packaging:**

The key packaging benefit: **the existing iOS framework binary is reused as-is**. The KMP Kotlin/Native framework links against the same binary and calls the same C symbols. No changes to the native build are needed.

For HERE SDK specifically:
- The `heresdk.framework` already contains C++ core + CBridge C/C++ code.
- The Swift layer can optionally remain for non-KMP customers.
- The KMP Kotlin/Native framework is a **separate artifact** that links against `heresdk.framework`.
- Both KMP and Swift customers can use the same underlying framework binary.

---

## 7. Phased Delivery

1. **Spike:** Confirm the collision-handling assumption in §2.5 (run `swift` + a stub `kmp-native` generator that also instantiates `CBridgeGenerator` in the same invocation, check `SplitSourceSetCache`/`checkForFileNameCollisions` behavior) — this determines whether §5.3 needs a refactor before any template work starts, or not.

2. **`commonMain` expect generator** on a small IDL subset (structs + simple interfaces, no generics/collections) — validate expect/actual signature equality against a hand-written JVM actual before generating either actual automatically.

3. **`androidMain` actual** — new `JniTemplates`-based templates; get a JVM-only KMP module compiling and passing existing Android functional tests.

4. **`iosMain` actual** via `cbridge` + `cinterop` — structs/enums first (no proxy cache needed), then interfaces/classes (proxy cache + lifetime).

5. **Build glue** (§6) + CI.

6. **Coverage pass:** generics, collections, `@Async`/callbacks, bring `kmp` generator parity with what `kotlin`/`swift` already support.

---

## 8. File Modification Checklist

*This checklist references the actual Gluecodium architecture (Mustache templates + Kotlin backend logic).*

1. **`gluecodium/src/main/java/com/here/gluecodium/Gluecodium.kt`**
   - Add validation for `kmp-common`, `kmp-jvm`, `kmp-native` options.
   - Register the new generator pipeline.

2. **`gluecodium/src/main/java/com/here/gluecodium/generator/common/GeneratorOptions.kt`**
   - Add new fields: `kmpPackages`, `kmpInternalPackages`, `kmpNativeTargets: List<String>`.
   - Add `kmpNameRules` `Configuration` loaded from a new `namerules/kmp.properties`.

3. **`gluecodium/src/main/java/com/here/gluecodium/generator/kmp/`** (New Package)
   - `common/KmpCommonGenerator.kt`: Generates `commonMain` `expect` declarations. Reuses `KotlinNameRules` for public name parity.
   - `jvmActual/KmpJvmActualGenerator.kt`: Sibling of `JavaGenerator`/`KotlinGenerator`; imports `JniTemplates` directly. Generates `androidMain`/`jvmMain` `actual` classes with JNI calls.
   - `nativeActual/KmpNativeActualGenerator.kt`: Imports `CBridgeGenerator`/`CBridgeNameResolver` directly (like `SwiftGenerator` does). Generates `iosMain`/`appleMain` `actual` classes with cinterop calls.
   - `KmpNameResolver.kt`: Name resolution for common/Android/iOS Kotlin (may extend or reuse `KotlinNameRules`).
   - `KmpGeneratorPredicates.kt`: Predicates for template logic.

4. **`gluecodium/src/main/resources/templates/kmp/`** (New Directory)
   - `common/` — `commonMain` templates:
     - `KmpClass.mustache`: `expect class` declarations.
     - `KmpInterface.mustache`: `expect interface` declarations.
     - `KmpStruct.mustache`: `data class` declarations.
     - `KmpEnum.mustache`: `enum class` declarations.
   - `android/` — `androidMain`/`jvmMain` templates:
     - `AndroidClass.mustache`: `actual class` with JNI calls.
   - `ios/` — `iosMain`/`appleMain` templates:
     - `IosClass.mustache`: `actual class` with CBridge cinterop calls.
     - `IosClassConversion.mustache`: `copyFromCType`/`moveToCType`/`copyToCType`/`moveToCType`.
     - `IosWrapperCache.mustache`: Kotlin wrapper cache + type repository.
     - `IosCollections.mustache`: List/Map/Set conversion functions.
   - `cinterop/` — cinterop definition file template:
     - `CInteropDef.mustache`: Generates `.def` files pointing at CBridge headers.

5. **`gluecodium/src/main/resources/namerules/kmp.properties`** (New File)
   - Naming rules for KMP output (can initially mirror `kotlin.properties`).

6. **`gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator`**
   - Register the three new generators: `KmpCommonGenerator`, `KmpJvmActualGenerator`, `KmpNativeActualGenerator`.

7. **`gluecodium/src/main/java/com/here/gluecodium/cli/OptionReader.kt`**
   - Add `kmp-common`, `kmp-jvm`, `kmp-native` to the list of accepted generators.

8. **Reuse existing generators (no modification needed):**
   - `CBridgeGenerator.kt` — generates C headers + impl (reused as-is for iOS).
   - `CBridgeNameResolver.kt` — resolves CBridge C function names (reused by KMP name resolver).
   - `JniTemplates` / JNI generator — generates C++ JNI bindings (reused as-is for Android).

---

## 9. Testing Strategy

1. **Unit Tests:**
   - Verify that `commonMain` generation produces `expect` keywords.
   - Verify that type mapping resolves to Kotlin standard library types (not `java.*`).
   - Verify that `iosMain` generation produces correct `cinterop` calls matching CBridge C function signatures.
   - Verify that `cinterop` `.def` files reference the correct CBridge headers.
   - Verify expect/actual signature conformance (the watch item from §5.1).

2. **Functional Tests:**
   - Create a test C++ library with classes, structs, enums, interfaces, and lambdas.
   - Run Gluecodium with `kmp-common,kmp-jvm,kmp-native` flags (combined with `cpp,cbridge` for the native layer).
   - Verify output directory structure (`commonMain`, `androidMain`, `iosMain`, `cinterop/`).
   - **Compilation Test:** Attempt to compile the generated KMP project using Gradle for both Android and iOS targets.

3. **Integration Test:**
   - Run a "Hello World" call from Common Kotlin → Android JNI → C++.
   - Run a "Hello World" call from Common Kotlin → iOS cinterop → CBridge → C++.
   - Verify that the existing iOS framework binary (built with `swift` generator) works with the KMP `iosMain` bindings without recompilation.

4. **Native Teardown Tests (§5.3 Memory/Lifetime):**
   - Dedicated test pass for Kotlin/Native `Cleaner`/`finalize()` teardown ordering.
   - Verify no `pthread_mutex_lock`-on-destroyed-mutex or destructor-exception analogs.

---

## 10. Risks & Mitigations

| Risk | Mitigation |
| :--- | :--- |
| **Expect/actual signature divergence** | `expect`/`actual` requires exact signature match after each side's type-mapping. Add a dedicated conformance check (not an assumption) wherever `KotlinValueResolver`/`KotlinSignatureResolver` make target-specific decisions. |
| **Kotlin/Native ↔ C interop edge cases** | The CBridge C ABI is pure `extern "C"` with opaque handles — the simplest possible interop target for `cinterop`. This avoids Objective-C ARC/block complexity entirely. Validate with comprehensive functional tests. |
| **Memory management (GC vs. ref counting)** | Kotlin/Native GC is non-deterministic and uses `Cleaner`/`createCleaner`, not finalizers. Do not port JNI or Swift finalizer patterns directly — design teardown ordering from scratch with its own test pass. For critical paths, provide explicit `close()`/`release()` methods. |
| **Callback Handling (C++ → Kotlin)** | Interface proxies require Kotlin objects callable from C++. Reuse the existing CBridge `FunctionTable` + `CachedProxyBase` mechanism (plain function-pointer struct, not Dart isolate messaging). Generate Kotlin proxy implementations that implement the CBridge function table with Kotlin callbacks. |
| **Wrapper cache consistency** | Reuse `cbridge`'s existing proxy/wrapper cache (`CachedProxyBase.h`/`WrapperCacheImpl.mustache`) rather than building a second cache on the Kotlin/Native side — otherwise Swift and Kotlin/Native consumers of the same underlying C++ object could observe different identities, a real regression versus what `cbridge` already guarantees today. Sync with the C++ cache via the existing `_get_swift_object_from_wrapper_cache` / `_cache_swift_object_wrapper` C functions. |
| **Swift + KMP coexistence** | Both Swift and KMP can use the same framework binary. The CBridge C symbols are identical. Swift classes and Kotlin classes are separate wrapper types — no conflict. Ensure the framework exports all CBridge symbols (already the case). |
| **Type Safety across Platforms** | Nullability differences between JNI (Java) and Kotlin/Native. Enforce strict nullability in `commonMain` interfaces. Use Kotlin's nullable types consistently. |
| **`cinterop` build-step ordering** | `cinterop` must run after CBridge headers exist but before Kotlin/Native compilation. The existing `gluecodium-gradle` plugin is JVM/Android-oriented and likely doesn't model this dependency edge. Needs an explicit task graph (see §6) — potentially new territory for this repo's build tooling. |

---

## 11. Open Questions

- **Q1**: Does `gluecodium-gradle` already have any task-graph precedent for a multi-stage generate → external-tool → generate pipeline (haven't read it yet), or is the `cinterop` ordering genuinely new territory for this repo's build tooling?
- **Q2**: For §2.5 — is (a) (let both generators instantiate `CBridgeGenerator`, rely on collision detection) actually safe, or does `CBridgeGenerator`'s constructor have side effects (e.g. `CppNameCache` mutation) that make two instances in one process unsafe even if the *output* would collide-and-dedupe correctly?
- **Q3**: Target scope for v1 — Android + iOS only, or does parity with any existing desktop HERE SDK target matter for the first cut?

---

## 12. Relative Complexity Ranking

1. `androidMain` actual — low (new templates over an already-shared ABI)
2. `commonMain` expect — low/medium (mechanical once `KotlinNameRules` reuse is confirmed)
3. Build orchestration (§6) — medium, possibly higher depending on Q1
4. `iosMain` actual (structs/enums) — medium
5. `iosMain` actual (interfaces/classes, proxy cache, lifetime) — high — the JNI-teardown class of bug has a native-memory-manager analog here, plus whatever the answer to Q2 turns out to be

---

## 13. Environment Setup for Kotlin/Native and `cinterop`

This section describes the local development environment needed to develop, test, and debug KMP bindings — specifically the Kotlin/Native `cinterop` toolchain that the `iosMain`/`appleMain` source sets depend on.

### 13.1. Prerequisites

| Tool | Minimum Version | Purpose |
|---|---|---|
| **JDK** | 17 (OpenJDK or Temurin) | Required by Gradle and the Kotlin Gradle Plugin |
| **Kotlin Gradle Plugin** | 2.0+ (recommended 2.1.x) | KMP `expect`/`actual` support, `cinterop` Gradle task integration |
| **Xcode** | 15+ (with Command Line Tools) | Kotlin/Native iOS targets (`iosX64`, `iosArm64`, `iosSimulatorArm64`) require the Apple LLVM toolchain and SDK headers |
| **Kotlin/Native compiler** | Bundled with Kotlin Gradle Plugin (auto-downloaded) | Includes `cinterop` tool, `konan` toolchain, and platform sysroot |
| **CMake** | 3.23.1+ | Already required by Gluecodium; also drives native framework builds |
| **Ninja** | latest | Recommended build backend for Kotlin/Native (faster incremental) |
| **LLVM/Clang** | 14+ (Xcode-bundled is fine) | `cinterop` uses `libclang` to parse CBridge headers |

> **Note:** The Kotlin/Native compiler auto-downloads its own LLVM toolchain (`~/.konan/dependencies/`) on first build. You do **not** need a separate LLVM install unless you want to inspect generated bitcode manually.

### 13.2. Installing and Verifying

#### JDK

```bash
brew install openjdk@17
# macOS: symlink into /Library/Java/JavaVirtualMachines
sudo ln -sfn $(brew --prefix)/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk
# Verify
java -version   # → openjdk version "17.x.x"
```

#### Xcode & Command Line Tools

```bash
# Install Xcode from App Store, then:
sudo xcode-select -s /Applications/Xcode.app/Contents/DeveloperTools
xcodebuild -version        # → Xcode 15.x
xcrun --show-sdk-path      # → .../SDKs/iPhoneOS17.x.sdk
```

#### CMake & Ninja

```bash
brew install cmake ninja
cmake --version   # → cmake version 3.2x.x
ninja --version   # → 1.x.x
```

#### Kotlin/Native & `cinterop`

The Kotlin/Native toolchain is **not installed separately** — it's pulled in by the Kotlin Gradle Plugin automatically on first build. However, you can verify the `cinterop` binary directly:

```bash
# After a first Gradle build, the toolchain lands in:
ls ~/.konan/kotlin-native-prebuilt-*/bin/
# You should see: cinterop, konan, kotlinc-native, run_konan, etc.

# Verify cinterop is available via Gradle:
cd /path/to/kmp-test-project
./gradlew :cinteropMyDef --info   # (after configuring a cinterop task, see §13.4)

# Or run cinterop directly:
~/.konan/kotlin-native-prebuilt-*/bin/cinterop -help
```

### 13.3. `cinterop` Configuration for CBridge Headers

The `cinterop` tool parses C headers and generates a Kotlin klib with typed bindings. For the KMP generator, the `.def` file points at the CBridge headers produced by `CBridgeGenerator`.

**Generated `.def` file example:**
```def
# com_example_sdk.def
language = C

# Point at CBridge headers (generated by Gluecodium's cbridge generator)
headers = cbridge/include/MyClass.h cbridge/include/MyStruct.h cbridge/include/Common.h

# Kotlin package for the generated bindings
package = com.example.sdk.cbridge

# Link against the existing framework / shared library
linkerOpts = -lheresdk

# Optional: additional compiler flags for header parsing
compilerOpts = -I/path/to/cbridge/include -DBRIDGE_ONLY
```

**Gradle `cinterop` task configuration** (in the KMP module's `build.gradle.kts`):

```kotlin
kotlin {
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    // One cinterop task per .def file (or one per module)
    val cinteropCbridge by cinterops.creating {
        defFile("src/nativeInterop/cinterop/com_example_sdk.def")

        // Extra compiler opts if needed
        compilerOpts("-I/path/to/cbridge/include")

        // Extra linker opts if needed
        linkerOpts("-lheresdk")
    }

    sourceSets {
        val iosMain by creating {
            dependsOn(commonMain.get())
            // cinterop bindings are automatically available in iosMain
            // via the package declared in the .def file
        }
        val iosX64Main by getting { dependsOn(iosMain) }
        val iosArm64Main by getting { dependsOn(iosMain) }
        val iosSimulatorArm64Main by getting { dependsOn(iosMain) }
    }
}
```

**Key points:**

- `cinterop` runs **before** Kotlin/Native compilation, producing a `.klib` that the `iosMain` source set imports as a dependency.
- The `.klib` contains raw `CPointer`, `COpaquePointer`, `CFunction<...>` types mapped from the C headers.
- The generated Kotlin `actual` classes call through these raw bindings — the same architectural role as Swift's `CBridgeClassConversion` layer.
- If the CBridge headers change (e.g., a new function is added), `cinterop` must re-run to regenerate the `.klib`. Gradle tracks `.def` file and header timestamps for incremental builds.

### 13.4. Build Task Ordering

The full KMP build involves a multi-stage pipeline:

```
Stage 1: Gluecodium generates code
  ┌─────────────────────────────────────────────────────────┐
  │ cpp generator      → C++ abstract classes (.h/.cpp)     │
  │ cbridge generator  → C headers + impl (.h/.cpp)          │
  │ jni generator      → JNI C++ glue (.cpp)                 │
  │ kmp-common         → commonMain expect decls (.kt)       │
  │ kmp-jvm            → androidMain actual (.kt)            │
  │ kmp-native         → iosMain actual (.kt) + .def files   │
  └─────────────────────────────────────────────────────────┘
                           │
Stage 2: Native compilation (CMake)
  ┌─────────────────────────────────────────────────────────┐
  │ C++ core + CBridge + JNI glue → compiled .so / .framework │
  └─────────────────────────────────────────────────────────┘
                           │
Stage 3: cinterop (Gradle, per native target)
  ┌─────────────────────────────────────────────────────────┐
  │ cinterop .def → .klib (parses CBridge C headers)         │
  └─────────────────────────────────────────────────────────┘
                           │
Stage 4: Kotlin/Native compilation (Gradle)
  ┌─────────────────────────────────────────────────────────┐
  │ iosMain actual (.kt) + .klib → .framework / .klib        │
  └─────────────────────────────────────────────────────────┘
```

**In Gradle terms, the task dependencies are:**

```kotlin
tasks.named("cinteropCbridgeIosX64") {
    dependsOn("generateCbridgeHeaders")   // Stage 1 output
    dependsOn("buildNativeFramework")      // Stage 2 output (C headers must exist)
}

tasks.named("compileKotlinIosX64") {
    dependsOn("cinteropCbridgeIosX64")     // Stage 3 must complete before Stage 4
}

tasks.named("compileKotlinIosArm64") {
    dependsOn("cinteropCbridgeIosArm64")
}

tasks.named("compileKotlinIosSimulatorArm64") {
    dependsOn("cinteropCbridgeIosSimulatorArm64")
}
```

### 13.5. Debugging `cinterop` Issues

Common problems and solutions:

| Problem | Cause | Solution |
|---|---|---|
| `cinterop` fails to find headers | `.def` file `headers` path is relative to wrong directory | Use absolute paths or `compilerOpts = -I<abs-path>`; verify with `cinterop -verbose` |
| `undefined symbol` at link time | CBridge symbols not exported from framework / `.so` | Ensure `extern "C"` visibility; check with `nm -gU libheresdk.so` / `otool -L` |
| Type mismatch between `cinterop` output and `actual` class | CBridge header types differ from what Gluecodium's KMP templates assumed | Inspect generated `.klib` with `konan-metadata` or check `cinterop` output in `build/classes/kotlin/iosX64/main/` |
| `cinterop` parses Obj-C++ in headers | CBridge headers contain `#import` or Obj-C syntax | CBridge headers are pure C — if Obj-C++ leaks in, file a bug; work around with `compilerOpts = -x c` |
| Build fails on macOS with "no SDK found" | Xcode path not set | Run `sudo xcode-select -s /Applications/Xcode.app/Contents/DeveloperTools` |
| Kotlin/Native compiler OOM | Large CBridge surface area | Increase `konan` memory: `./gradlew -Dorg.gradle.jvmargs="-Xmx4g"` or set `kotlinc.native.freeCompilerArgs` |

### 13.6. Quick Smoke-Test Project

To validate the environment before any Gluecodium changes, create a minimal KMP project that calls a hand-written CBridge header:

```bash
mkdir kmp-smoke-test && cd kmp-smoke-test
gradle init --type kotlin-multiplatform
```

**`src/nativeInterop/cinterop/smoke.def`:**
```def
language = C
headers = smoke.h
package = smoke.cbridge
```

**`src/nativeInterop/cinterop/smoke.h`:**
```c
#pragma once
#include <stdint.h>
typedef void* _baseRef;
extern _baseRef smoke_create();
extern int32_t smoke_do_something(_baseRef handle, int32_t input);
extern void smoke_release_handle(_baseRef handle);
```

**`src/iosMain/kotlin/SmokeTest.kt`:**
```kotlin
import smoke.cinterop.*

actual class SmokeTest actual constructor() {
    private val handle: _baseRef = smoke_create()!!

    actual fun doSomething(input: Int): Int {
        return smoke_do_something(handle, input)
    }

    protected fun finalize() {
        smoke_release_handle(handle)
    }
}
```

**`src/commonMain/kotlin/SmokeTest.kt`:**
```kotlin
expect class SmokeTest() {
    fun doSomething(input: Int): Int
}
```

Build and run on iOS simulator:
```bash
./gradlew iosSimulatorArm64Test
```

If this compiles and runs, the `cinterop` toolchain is correctly set up and ready for Gluecodium-generated bindings.

---

## 14. Getting Started (Immediate Steps)

1. **Set up the environment** (§13): verify JDK 17, Xcode, CMake, Ninja, and run the `cinterop` smoke test.
2. Clone Gluecodium Repository.
3. Create a feature branch `feature/kotlin-multiplatform`.
4. **Spike (§7 step 1):** Confirm the collision-handling assumption in §2.5.
5. Implement **Phase 1 (Config)** — `GeneratorOptions` fields, `OptionReader` entries, `namerules/kmp.properties`.
6. Create a "Hello World" hardcoded generator to output the file structure.
7. Begin implementation of **`commonMain` expect generator** (§5.1).
8. For **`iosMain` actual** (§5.3), start by:
   a. Running Gluecodium with `cpp,swift` on a test `.lime` file.
   b. Inspecting the generated `cbridge/include/*.h` headers.
   c. Writing a manual `cinterop` `.def` file and a hand-written Kotlin wrapper.
   d. Verify the Kotlin wrapper can call the CBridge C functions from a Kotlin/Native iOS target.
   e. Once the manual approach is validated, automate it with templates.