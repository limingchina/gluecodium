Here is a comprehensive `plan.md` detailing the implementation of Kotlin Multiplatform (KMP) binding support for Gluecodium. (Generated with GLM 5.2)
***
# Plan: Add Kotlin Multiplatform (KMP) Binding Support to Gluecodium
## 1. Overview
**Objective:** Extend Gluecodium to generate Kotlin Multiplatform (KMP) source sets, enabling the sharing of Kotlin code between Android and iOS platforms while leveraging existing C++ core logic.
**Current State:** Gluecodium generates platform-specific bindings:
*   **Android:** Kotlin/Java bindings using JNI.
*   **iOS:** Swift bindings (interacting with C++ via Objective-C++).
**Target State:** A new generator module that produces:
1.  `commonMain`: Kotlin interfaces and data classes (the "API" layer).
2.  `androidMain`: `actual` implementations using JNI (bridging to existing C++).
3.  `nativeMain` (or `iosMain`): `actual` implementations interacting with the C++ layer (bridging to existing Swift/C++ logic).
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
3.  **Native/iOS Source (`nativeMain`):**
    *   Generates `actual` classes.
    *   Uses `kotlinx.cinterop` to talk to C++ (or Objective-C wrappers).
    *   *Decision:* For iOS, Gluecodium currently generates Swift. For KMP, we need a Kotlin/Native bridge. This will likely involve generating a C wrapper or Objective-C wrapper that Kotlin/Native can consume via `cinterop`.
### 2.2. Directory Structure Output
The output directory will follow the standard KMP `sourceSets` structure:
```text
output/
└── kotlin-multiplatform/
    ├── build.gradle.kts       (Optional: Template build file)
    └── src/
        ├── commonMain/kotlin/com/example/...
        ├── androidMain/kotlin/com/example/...
        └── nativeMain/kotlin/com/example/...
```
---
## 3. Implementation Plan
### Phase 1: Model & Configuration Setup
**Step 1.1: Configuration Options**
*   Modify `Gluecodium.kt` (or the main entry point) to accept a new generator option: `kotlin-multiplatform`.
*   Add configuration for common package naming (e.g., handling suffix differences between Android and iOS if necessary).
**Step 1.2: LIME Model Extensions**
*   Analyze the existing LIME model. No changes should be needed to the core IDL, but the **generator context** needs to distinguish between "Interface Definition" and "Implementation Details".
*   Ensure model properties (e.g., `Platform`). are accessible to filter logic.
### Phase 2: Common Generator (`commonMain`)
**Step 2.1: Create `KMPCommonGenerator`**
*   Create a new generator class extending the base generator logic.
*   **Templates (`commonMain.ftl`):**
    *   **Classes:** Generate `expect class MyClass { ... }` or interfaces.
    *   **Structs:** Generate `data class` (standard KMP supports these).
    *   **Enums:** Generate `enum class`.
    *   **Exceptions:** Define custom exception wrappers.
**Step 2.3: Type Mapping**
*   Ensure the type mapper uses Kotlin common types (e.g., `String`, `List`, `Map`) instead of platform-specific types like `java.util.List` or Android-specific `Context`.
### Phase 3: Android Implementation (`androidMain`)
**Step 3.1: Adapt existing JNI Logic**
*   The current Android generator produces a full class. We need to refactor this.
*   **Template Modification:** instead of generating a standalone class, generate an `actual class` that implements the `expect` interface.
*   **Implementation:**
    ```kotlin
    // actual class MyClassImpl : MyClass {
    //    // JNI Calls go here
    // }
    ```
*   Reuse the existing C++ JNI generation logic (the `.cpp` files). The `.kt` files must now bind to the native library via `System.loadLibrary` within the actual class scope.
### Phase 4: iOS/Native Implementation (`nativeMain`)
*This is the most complex addition.*
**Step 4.1: C-Interop Strategy**
*   Gluecodium's C++ layer needs to be exposed to Kotlin/Native via C headers.
*   **Action:** Reuse or extend the "Pure C" generator (if available) or generate a minimal C-wrapper over the C++ objects.
*   Alternatively, leverage the Objective-C generation: Kotlin/Native interacts well with Objective-C.
    *   *Path of least resistance:* Generate Kotlin code that imports the generated Objective-C headers (via `cinterop` definitions).
**Step 4.2: `nativeMain` Templates**
*   Generate `actual` implementations.
*   Use `foreignReference` annotations or direct `cinterop` calls to access the C++/ObjC memory.
*   Handle memory management (Smart pointers) carefully. Kotlin/Native has different GC interaction with C++ than JNI.
### Phase 5: Build System Integration
**Step 5.1: Gradle Plugin / Configuration**
*   Generate a boilerplate `build.gradle.kts` file configured for Multiplatform.
    ```kotlin
    kotlin {
        androidTarget()
        iosX64()
        iosArm64()
        sourceSets {
            val commonMain by getting { ... }
            val androidMain by getting { ... }
            val iosMain by creating { ... }
        }
    }
    ```
*   Ensure interop configuration (`cinterop`) is generated for the iOS target to link against the Gluecodium C++ libraries.
---
## 4. File Modification Checklist
*This checklist assumes standard Gluecodium architecture (FreeMarker templates + Java/Kotlin backend logic).*
1.  **`gluecodium/src/main/java/com/here/gluecodium/Gluecodium.kt`**
    *   Add validation for `kmp` option.
    *   Register the new generator pipeline.
2.  **`gluecodium/src/main/java/com/here/gluecodium/generator/kmp/`** (New Package)
    *   `KMPGenerator.kt`: Main logic to orchestrate the three source sets.
    *   `KMPModelBuilder.kt`: Adapts LIME model to KMP specific needs.
3.  **`gluecodium/src/main/resources/templates/kmp/`** (New Directory)
    *   `CommonClass.ftl`: Template for `expect` classes and interfaces.
    *   `AndroidActual.ftl`: Template for JNI implementation.
    *   `NativeActual.ftl`: Template for Kotlin/Native implementation.
4.  **`gluecodium/src/main/java/com/here/gluecodium/loader/`**
    *   Ensure LimeModel loader passes necessary metadata for KMP generation.
---
## 5. Testing Strategy
1.  **Unit Tests:**
    *   Verify that `commonMain` generation produces `expect` keywords.
    *   Verify that type mapping resolves to Kotlin standard library types (not `java.*`).
2.  **Functional Tests:**
    *   Create a test C++ library.
    *   Run Gluecodium with KMP flag.
    *   Verify output directory structure (`commonMain`, `androidMain`, `nativeMain`).
    *   **Compilation Test:** Attempt to compile the generated KMP project using Gradle.
3.  **Integration Test:**
    *   Run a "Hello World" call from Common Kotlin -> Android JNI -> C++.
    *   Run a "Hello World" call from Common Kotlin -> iOS Native -> C++.
## 6. Risks & Mitigations
| Risk | Mitigation |
| :--- | :--- |
| **Kotlin/Native C++ Interop Complexity** | Kotlin/Native cannot talk to C++ directly easily. We must rely on C-wrappers or the existing Objective-C generator. We will prioritize the **Objective-C bridge** approach as it is already mature in Gluecodium. |
| **Type Safety across Platforms** | Nullability differences between JNI (Java) and Swift/Kotlin-Native. Enforce strict nullability in `commonMain` interfaces. |
| **Callback Handling** | Implementing interfaces in C++ that are called from Kotlin (Listeners) requires proxy generation for both platforms. Reuse existing listener logic. |
---
## 7. Getting Started (Immediate Steps)
1.  Clone Gluecodium Repository.
2.  Create a feature branch `feature/kotlin-multiplatform`.
3.  Implement **Phase 1 (Config)** to allow the tool to accept the new flag.
4.  Create a "Hello World" hardcoded generator to output the file structure.
5.  Begin implementation of **Phase 2 (Common Generator)**.
