# Plan: Add Kotlin Multiplatform (KMP) Binding Support to Gluecodium

## 1. Overview

**Objective:** Extend Gluecodium to generate Kotlin Multiplatform (KMP) source sets, enabling the sharing of Kotlin code between Android and iOS platforms while leveraging existing C++ core logic.

**Current State:** Gluecodium generates platform-specific bindings:
*   **Android:** Kotlin/Java bindings using JNI.
*   **iOS:** Swift bindings (interacting with C++ via a pure-C CBridge layer).

**Target State:** A new generator module that produces:
1.  `commonMain`: Kotlin interfaces and data classes (the "API" layer).
2.  `androidMain`: `actual` implementations using JNI (bridging to existing C++).
3.  `iosMain`: `actual` implementations that reuse the existing **CBridge C ABI** layer via Kotlin/Native `cinterop`, eliminating the need for Swift or Objective-C interop.

---

## 2. Architecture & Design Strategy

KMP support requires a shift from "generate a class" to "generate an interface (expect) and an implementation (actual)."

### 2.1. The "Expect/Actual" Pattern

Gluecodium will generate three distinct source sets:

1.  **Common Source (`commonMain`):**
    *   Generates Kotlin `interface`s, `data class`es, and `enum class`es.
    *   Marked as `expect` for classes requiring platform-specific implementation.
    *   Contains no C++ interop logic.
2.  **Android Source (`androidMain`):**
    *   Generates `actual` classes.
    *   Wraps the existing JNI C++ bridge code.
    *   Uses the existing `JniReference` handling logic.
3.  **iOS Source (`iosMain`):**
    *   Generates `actual` classes.
    *   Reuses the existing **CBridge C ABI** (pure C `extern "C"` functions with `_baseRef` opaque handles) as the interop target.
    *   Generates `cinterop` `.def` definition files pointing at the existing `cbridge/include/*.h` headers.
    *   Generates Kotlin wrappers that call the CBridge C functions and manage handle lifetimes in Kotlin.

### 2.2. Current iOS Binding Architecture

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
- The **Dart generator** already follows a similar pattern: generating C wrappers (`ffi/*.h`) + Dart wrappers that call through `dart:ffi`. The KMP `iosMain` approach mirrors this with `cinterop` instead of `dart:ffi`.

### 2.3. KMP iOS Architecture: CBridge-cinterop Reuse

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

**Why reuse CBridge instead of Swift or Objective-C:**

| Aspect | CBridge C ABI (Recommended) | Objective-C | Swift |
|---|---|---|---|
| Kotlin/Native interop | ✅ `cinterop` (native support) | ⚠️ Works but more complex (ARC, blocks) | ❌ Not supported |
| Already in framework | ✅ Compiled into existing `.framework` | ❌ Would need new generation | ❌ Cannot call from Kotlin |
| Maturity | ✅ Battle-tested in production | ❌ Gluecodium doesn't generate Obj-C | ❌ N/A |
| Memory management | ✅ Explicit handle ref/unref | ⚠️ ARC interaction complexity | ❌ N/A |
| Framework reuse | ✅ Same binary, same C symbols | ❌ New native code needed | ❌ N/A |

### 2.4. Directory Structure Output

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

## 3. Implementation Plan

### Phase 1: Model & Configuration Setup

**Step 1.1: Configuration Options**
*   Modify `Gluecodium.kt` (or the main entry point) to accept a new generator option: `kotlin-multiplatform`.
*   Add configuration for common package naming (e.g., handling suffix differences between Android and iOS if necessary).

**Step 1.2: LIME Model Extensions**
*   Analyze the existing LIME model. No changes should be needed to the core IDL, but the **generator context** needs to distinguish between "Interface Definition" and "Implementation Details".
*   Ensure model properties (e.g., `Platform`) are accessible to filter logic.

### Phase 2: Common Generator (`commonMain`)

**Step 2.1: Create `KMPCommonGenerator`**
*   Create a new generator class extending the base generator logic.
*   **Templates:**
    *   **Classes:** Generate `expect class MyClass { ... }` or interfaces.
    *   **Structs:** Generate `data class` (standard KMP supports these).
    *   **Enums:** Generate `enum class`.
    *   **Exceptions:** Define custom exception wrappers.

**Step 2.2: Type Mapping**
*   Ensure the type mapper uses Kotlin common types (e.g., `String`, `List`, `Map`) instead of platform-specific types like `java.util.List` or Android-specific `Context`.

### Phase 3: Android Implementation (`androidMain`)

**Step 3.1: Adapt existing JNI Logic**
*   The current Android generator produces a full class. We need to refactor this.
*   **Template Modification:** Instead of generating a standalone class, generate an `actual class` that implements the `expect` interface.
*   **Implementation:**
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
*   Reuse the existing C++ JNI generation logic (the `.cpp` files). The `.kt` files must now bind to the native library via `System.loadLibrary` within the actual class scope.

### Phase 4: iOS Implementation (`iosMain`)

*This phase reuses the existing CBridge C ABI layer — no new native code generation is required for iOS.*

**Step 4.1: CBridge Reuse Strategy**

The existing CBridge generator (`CBridgeGenerator.kt`) already produces:
- **C headers** (`cbridge/include/*.h`) — pure `extern "C"` functions with `_baseRef` opaque handles
- **C++ implementations** (`cbridge/src/*.cpp`) — Objective-C++ that bridges to the C++ core
- **Common helpers** — `BaseHandleImpl.h`, `StringHandle.h`, `BuiltinHandle.h`, `ByteArrayHandle.h`, `WrapperCache.h`, etc.

These are **already compiled into the existing iOS framework binary**. The KMP generator does **not** need to regenerate any native code for iOS. It only needs to:

1.  Generate `cinterop` definition files that point Kotlin/Native at the existing CBridge headers
2.  Generate Kotlin `actual` classes that call the C functions and manage handles

**Step 4.2: Generate `cinterop` Definition Files**

For each LIME package/module, generate a `.def` file:
```def
// com_example_sdk.def
language = C
headers = cbridge/include/MyClass.h cbridge/include/MyStruct.h ...
package = com.example.sdk.cbridge
linkerOpts = -lheresdk
```

This makes all CBridge C functions available to Kotlin/Native as Kotlin functions via `kotlinx.cinterop`.

**Step 4.3: Generate `iosMain` Kotlin Actual Classes**

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

**Step 4.4: Generate Kotlin Conversion Functions**

Port the Swift conversion layer to Kotlin. These are the Kotlin equivalents of `SwiftClassConversion.mustache`:

| Swift Function | Kotlin Equivalent | Purpose |
|---|---|---|
| `copyFromCType(_ handle: _baseRef) -> MyClass` | `fun copyFromCType(handle: _baseRef): MyClass` | Construct wrapper from handle (non-owning) |
| `moveFromCType(_ handle: _baseRef) -> MyClass` | `fun moveFromCType(handle: _baseRef): MyClass` | Construct wrapper from handle (owning, releases on GC) |
| `copyToCType(_ swiftClass: MyClass) -> RefHolder` | `fun copyToCType(obj: MyClass): RefHolder` | Extract handle from wrapper (non-owning copy) |
| `moveToCType(_ swiftClass: MyClass) -> RefHolder` | `fun moveToCType(obj: MyClass): RefHolder` | Extract handle from wrapper (owning move) |
| `_CBridgeInitMyClass(handle:)` | `fun cbBridgeInit(handle: _baseRef): Any` | Type-repository dispatch for interface proxies |

**Step 4.5: Kotlin Wrapper Cache & Type Repository**

Replace Swift's `Unmanaged<AnyObject>` + CBridge cache with Kotlin equivalents:

```kotlin
// Wrapper cache: maps C++ pointer → Kotlin wrapper (prevents duplicate wrappers)
private val wrapperCache = mutableMapOf<_baseRef, MyClass>()

// Type repository: maps type-id string → constructor function (for interface proxies)
private val typeRepository = mutableMapOf<String, (_baseRef) -> Any>()
```

**Step 4.6: Memory Management**

Kotlin/Native GC differs from both JNI (no GC across boundary) and Swift (ARC). Key considerations:
- Use Kotlin `Cleaner` (or `finalize()`) to call `MyClass_release_handle()` when the Kotlin wrapper is collected.
- For non-owning references (copied handles), do not release — the original owner holds the reference.
- For interface proxies (C++ → Kotlin callbacks), use the existing `CachedProxyBase` mechanism via CBridge.

### Phase 5: Build System Integration

**Step 5.1: Gradle Plugin / Configuration**
*   Generate a boilerplate `build.gradle.kts` file configured for Multiplatform.
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
*   Generate `cinterop` configuration that links against the existing iOS framework's CBridge headers.

**Step 5.2: Framework Packaging**

The key packaging benefit: **the existing iOS framework binary is reused as-is**. The KMP Kotlin/Native framework links against the same binary and calls the same C symbols. No changes to the native build are needed.

For HERESDK specifically:
- The `heresdk.framework` already contains C++ core + CBridge C/C++ code
- The Swift layer can optionally remain for non-KMP customers
- The KMP Kotlin/Native framework is a **separate artifact** that links against `heresdk.framework`
- Both KMP and Swift customers can use the same underlying framework binary

---

## 4. File Modification Checklist

*This checklist references the actual Gluecodium architecture (Mustache templates + Kotlin backend logic).*

1.  **`gluecodium/src/main/java/com/here/gluecodium/Gluecodium.kt`**
    *   Add validation for `kmp` option.
    *   Register the new generator pipeline.

2.  **`gluecodium/src/main/java/com/here/gluecodium/generator/kmp/`** (New Package)
    *   `KMPGenerator.kt`: Main logic to orchestrate the three source sets + cinterop defs.
    *   `KMPNameResolver.kt`: Name resolution for common/Android/iOS Kotlin.
    *   `KMPGeneratorPredicates.kt`: Predicates for template logic.

3.  **`gluecodium/src/main/resources/templates/kmp/`** (New Directory)
    *   `common/` — `commonMain` templates:
        *   `KmpClass.mustache`: `expect class` declarations.
        *   `KmpInterface.mustache`: `expect interface` declarations.
        *   `KmpStruct.mustache`: `data class` declarations.
        *   `KmpEnum.mustache`: `enum class` declarations.
    *   `android/` — `androidMain` templates:
        *   `AndroidClass.mustache`: `actual class` with JNI calls.
    *   `ios/` — `iosMain` templates:
        *   `IosClass.mustache`: `actual class` with CBridge cinterop calls.
        *   `IosClassConversion.mustache`: `copyFromCType`/`moveToCType`/`copyToCType`/`moveToCType`.
        *   `IosWrapperCache.mustache`: Kotlin wrapper cache + type repository.
        *   `IosCollections.mustache`: List/Map/Set conversion functions.
    *   `cinterop/` — cinterop definition file template:
        *   `CInteropDef.mustache`: Generates `.def` files pointing at CBridge headers.

4.  **Reuse existing generators (no modification needed):**
    *   `CBridgeGenerator.kt` — generates C headers + impl (reused as-is for iOS).
    *   `CBridgeNameResolver.kt` — resolves CBridge C function names (reused by KMP name resolver).
    *   JNI generator — generates C++ JNI bindings (reused as-is for Android).

5.  **`gluecodium/src/main/resources/META-INF/services/`**
    *   Register the new KMP generator in ServiceLoader configuration.

6.  **`gluecodium/src/main/java/com/here/gluecodium/cli/OptionReader.kt`**
    *   Add `kotlin-multiplatform` (or `kmp`) to the list of accepted generators.

---

## 5. Testing Strategy

1.  **Unit Tests:**
    *   Verify that `commonMain` generation produces `expect` keywords.
    *   Verify that type mapping resolves to Kotlin standard library types (not `java.*`).
    *   Verify that `iosMain` generation produces correct `cinterop` calls matching CBridge C function signatures.
    *   Verify that `cinterop` `.def` files reference the correct CBridge headers.

2.  **Functional Tests:**
    *   Create a test C++ library with classes, structs, enums, interfaces, and lambdas.
    *   Run Gluecodium with `kmp` flag (combined with `cpp,cbridge` for the native layer).
    *   Verify output directory structure (`commonMain`, `androidMain`, `iosMain`, `cinterop/`).
    *   **Compilation Test:** Attempt to compile the generated KMP project using Gradle for both Android and iOS targets.

3.  **Integration Test:**
    *   Run a "Hello World" call from Common Kotlin → Android JNI → C++.
    *   Run a "Hello World" call from Common Kotlin → iOS cinterop → CBridge → C++.
    *   Verify that the existing iOS framework binary (built with `swift` generator) works with the KMP `iosMain` bindings without recompilation.

---

## 6. Risks & Mitigations

| Risk | Mitigation |
| :--- | :--- |
| **Kotlin/Native ↔ C interop edge cases** | The CBridge C ABI is pure `extern "C"` with opaque handles — the simplest possible interop target for `cinterop`. This avoids Objective-C ARC/block complexity entirely. Validate with comprehensive functional tests. |
| **Memory management (GC vs. ref counting)** | Kotlin/Native GC is non-deterministic. Use `Cleaner` or `finalize()` to release CBridge handles. For critical paths, provide explicit `close()`/`release()` methods. Mirror the Dart generator's `NativeBase` pattern which already solves this for FFI. |
| **Type Safety across Platforms** | Nullability differences between JNI (Java) and Kotlin/Native. Enforce strict nullability in `commonMain` interfaces. Use Kotlin's nullable types consistently. |
| **Callback Handling (C++ → Kotlin)** | Interface proxies require Kotlin objects callable from C++. Reuse the existing CBridge `FunctionTable` + `CachedProxyBase` mechanism. Generate Kotlin proxy implementations that implement the CBridge function table with Kotlin callbacks. |
| **Wrapper cache consistency** | The CBridge wrapper cache (`WrapperCache.h`) stores `void*` pointers. For Kotlin/Native, generate a parallel Kotlin-side cache (`MutableMap<_baseRef, Any>`) and sync with the C++ cache via the existing `_get_swift_object_from_wrapper_cache` / `_cache_swift_object_wrapper` C functions. |
| **Swift + KMP coexistence** | Both Swift and KMP can use the same framework binary. The CBridge C symbols are identical. Swift classes and Kotlin classes are separate wrapper types — no conflict. Ensure the framework exports all CBridge symbols (already the case). |

---

## 7. Getting Started (Immediate Steps)

1.  Clone Gluecodium Repository.
2.  Create a feature branch `feature/kotlin-multiplatform`.
3.  Implement **Phase 1 (Config)** to allow the tool to accept the new flag.
4.  Create a "Hello World" hardcoded generator to output the file structure.
5.  Begin implementation of **Phase 2 (Common Generator)**.
6.  For **Phase 4 (iOS)**, start by:
    a. Running Gluecodium with `cpp,swift` on a test `.lime` file.
    b. Inspecting the generated `cbridge/include/*.h` headers.
    c. Writing a manual `cinterop` `.def` file and a hand-written Kotlin wrapper.
    d. Verify the Kotlin wrapper can call the CBridge C functions from a Kotlin/Native iOS target.
    e. Once the manual approach is validated, automate it with templates.
