# AGENTS.md - AI Agent Guide for Gluecodium

## Project Overview

Gluecodium is a code generation tool that creates bindings between C++ and multiple platform languages (Java, Kotlin, Swift, and Dart). It enables cross-platform mobile development by generating C++ interfaces and corresponding platform-specific bindings for Android, iOS, macOS, Linux, and Flutter.

**Primary Purpose:** Generate C++ abstract classes and platform bindings from LimeIDL interface definitions, eliminating the need for manual conversion code.

**Supported Output Languages:**
- C++ (headers and minimal implementation files)
- Java/Kotlin (for Android via JNI)
- Swift (for iOS/macOS via CBridge)
- Dart (for Flutter via FFI)
- JavaScript/TypeScript (for WebAssembly via embind — in development, see `docs/js_binding_dev/`)

## Repository Structure

```
gluecodium/
├── gluecodium/           # Main source code (Gradle project)
│   └── src/main/
│       ├── java/com/here/gluecodium/
│       │   ├── Gluecodium.kt          # Main entry point
│       │   ├── cache/                 # Output file caching
│       │   ├── cli/                   # CLI option parsing
│       │   ├── generator/             # Code generators
│       │   │   ├── cpp/               # C++ generator
│       │   │   ├── java/              # Java generator
│       │   │   ├── kotlin/            # Kotlin generator
│       │   │   ├── swift/             # Swift generator (with CBridge)
│       │   │   ├── dart/              # Dart generator (with FFI)
│       │   │   └── common/            # Shared generator infrastructure
│       │   │   # (js/ — JS/embind generator, planned: see docs/js_binding_dev/js_binding_plan.md)
│       │   └── validator/             # LIME model validators
│       └── resources/
│           └── templates/             # Mustache templates for each language
│
├── lime-loader/         # LimeIDL parser (Gradle project)
│   ├── antlr/           # ANTLR grammar for LimeIDL
│   └── java/            # Parser implementation
│
├── lime-runtime/        # LIME model runtime (Gradle project)
│   └── java/            # Language-Independent Model (LIME) types
│
├── gluecodium-gradle/   # Gradle plugin for Gluecodium
│
├── functional-tests/    # Functional test suites
│   ├── functional/      # Main functional tests
│   ├── namerules/       # Custom naming rules tests
│   └── scripts/         # Build scripts for running tests
│
├── cmake/               # CMake toolchain for Gluecodium
│   └── modules/         # CMake modules
│
├── tools/               # Additional tools
│   └── launcher/        # Minimal launcher for running Gluecodium
│
├── examples/            # Example projects
│   └── calculator/      # Simple calculator example
│
└── docs/                # Documentation
    ├── guide.md         # User guide
    ├── lime_idl.md      # LimeIDL language reference
    ├── internal/        # Internal development docs
    └── [various feature docs]
```

## Key Concepts

### LimeIDL (Input Language)

LimeIDL is the interface definition language used by Gluecodium. Syntax is inspired by Kotlin/Swift, designed to be compact and readable.

**File Structure:**
```lime
package com.example.myapp

class MyClass {
    fun myFunction(param: String): Int
    property myProperty: String
}

interface MyInterface {
    fun callback(result: Result): Void
}

struct MyStruct {
    field1: String
    field2: Int = 42  // with default value
}

enum MyEnum { VALUE1, VALUE2 }
```

**Key Elements:**
- `class`: Abstract class in C++, concrete wrapper in platform languages
- `interface`: Interface/protocol in all languages, can be implemented in platform code
- `struct`: Value type, passed by copy across language boundaries
- `enum`: Enumeration type
- `exception`: Error type representation

### LIME Model (Internal Representation)

The Language-Independent ModEl (LIME) is an intermediate tree representation parsed from LimeIDL files. It serves as the input for all generators.

### Generators

Each generator:
1. Filters the LIME model (based on `@Skip` and `@EnableIf` attributes)
2. Validates the model (generator-specific validation)
3. Collects imports/includes
4. Applies Mustache templates to generate code
5. Resolves element names (via name resolvers)

**Generator Types:**
- **C++ Generator**: Headers with abstract classes, minimal implementation files
- **Java/Kotlin Generators**: Java/Kotlin files + JNI bindings (C/C++)
- **Swift Generator**: Swift files + CBridge (Objective-C compatible C/C++ bindings)
- **Dart Generator**: Dart files + FFI bindings (C/C++)
- **JavaScript/WebAssembly Generator** (in development): TypeScript `.d.ts` stubs + embind C++
  bindings (`EMSCRIPTEN_BINDINGS` blocks) cross-compiled by `em++` into a `.wasm` binary.
  Unlike pybind11/Dart/Swift, the *entire* dependency graph must be compiled with the Emscripten
  toolchain. See `docs/js_binding_dev/js_binding_plan.md` for the phased plan and
  `docs/js_binding_dev/spike_phase0_results.md` for validated spike findings (notably: embind
  needs custom casters for `Return<T, E>` and `std::optional<T>`; multiple inheritance is handled
  via primary-base registration + flattened secondary-parent members).

### Mustache Templates

All generators use Mustache templates (via Trimou engine) located in `gluecodium/src/main/resources/templates/`. Templates are organized by language and type.

## Build and Development

### Prerequisites

- **Java JDK 8+** (for running Gluecodium)
- **Gradle** (build system)
- For functional tests:
  - CMake 3.19.3+
  - Ninja
  - Android SDK (for Android tests)
  - Swift SDK (for Swift tests)
  - Dart SDK (for Dart tests)

### Building the Project

```bash
# Build entire project
./gradlew build

# Run unit tests
./gradlew test

# Publish to local Maven repository
./gradlew publishToLocalMaven
```

### Running Gluecodium

**Using Launcher Tool:**
```bash
cd tools/launcher
gradle run --args="-help"
gradle run --args="-input <lime-dir> -output <output-dir> -generators cpp,swift"
```

**Using CLI:**
```bash
./generate -help
./generate -input <input-folder> -output <output-folder> -generators <generators>
```

**Command Line Options:**
- `-input`: Input LimeIDL files/folders
- `-output`: Output directory for generated code
- `-generators`: List of generators (cpp, java, kotlin, swift, dart)
- `-cache`: Enable output file caching
- `-options <file>`: Read options from .properties file

### Testing

**Unit Tests:**
```bash
./gradlew test
```

**Smoke Tests (acceptance tests):**
Located in `gluecodium/src/test/resources/smoke/`. Compare generated output against reference files.

**Functional Tests:**
Large-scale black-box tests that compile generated code and run platform-specific tests.

```bash
# Android functional tests
functional-tests/scripts/build-android-functional --publish --hostOnly

# Swift functional tests
functional-tests/scripts/build-swift-functional --publish

# C++ functional tests
functional-tests/scripts/build-cpp-functional --publish

# Dart functional tests
functional-tests/scripts/build-dart-functional --publish
```

### Using CMake Toolchain

Gluecodium can be integrated into CMake-based projects:

```cmake
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/path/to/cmake/modules")
include(Gluecodium)

# Add LimeIDL sources
set_property(TARGET mylibrary APPEND PROPERTY GLUECODIUM_LIME_SOURCES
             "path/to/file1.lime"
             "path/to/file2.lime")

# Configure options
set_property(TARGET mylibrary PROPERTY GLUECODIUM_CPP_NAMESPACE "myapp")
set_property(TARGET mylibrary PROPERTY GLUECODIUM_JAVA_PACKAGE "com.example.myapp")
```

### Using Gradle Plugin

```groovy
buildscript {
    dependencies {
        classpath "com.here.gluecodium:gluecodium-gradle:5.8.0"
    }
}

apply plugin: 'gluecodium.gradle'

gluecodium {
    source = fileTree("${rootDir}/lime")
    outputDirectory = file("$buildDir/generated-src/gluecodium")
    javaPackage = 'com.example.myapp'
    cppNamespace = 'myapp'
}
```

## Code Generation Workflow

1. **Parse LimeIDL**: ANTLR parser creates AST from LimeIDL files
2. **Create LIME Model**: Convert AST to LIME model tree
3. **Validate Model**: Run validators on LIME model
4. **Select Generators**: Based on command line options
5. **Generate Code**: Each generator applies Mustache templates
6. **Write Output**: Write generated files to output directory (with optional caching)

## Important Files to Know

- `gluecodium/src/main/java/com/here/gluecodium/Gluecodium.kt`: Main entry point
- `gluecodium/src/main/java/com/here/gluecodium/cli/OptionReader.kt`: CLI parser
- `gluecodium/src/main/java/com/here/gluecodium/generator/common/Generator.kt`: Generator interface
- `lime-loader/src/main/antlr/LimeIDL.g4`: ANTLR grammar
- `lime-runtime/src/main/java/com/here/gluecodium/model/lime/`: LIME model types
- `functional-tests/functional/input/lime/`: Example LimeIDL files for testing

## Common Tasks

### Adding a New LimeIDL Feature

1. Update ANTLR grammar (`lime-loader/src/main/antlr/LimeIDL.g4`)
2. Update LIME model types (`lime-runtime/src/main/java/com/here/gluecodium/model/lime/`)
3. Update parser (`lime-loader/src/main/java/com/here/gluecodium/loader/`)
4. Update validators if needed (`gluecodium/src/main/java/com/here/gluecodium/validator/`)
5. Update generators:
   - Add Mustache templates in `gluecodium/src/main/resources/templates/<language>/`
   - Update name resolvers in `gluecodium/src/main/java/com/here/gluecodium/generator/<language>/`
6. Add functional tests in `functional-tests/functional/input/lime/`
7. Update smoke tests references

### Adding a New Generator

1. Implement `Generator` interface (`gluecodium/src/main/java/com/here/gluecodium/generator/common/Generator.kt`)
2. Create Mustache templates in `gluecodium/src/main/resources/templates/<language>/`
3. Create name resolvers
4. Create import/include resolvers
5. Add to ServiceLoader configuration (`gluecodium/src/main/resources/META-INF/services/`)
6. Add CLI options support in `OptionReader.kt`
7. Add validators if needed
8. Add functional tests

### Fixing a Bug in Generated Code

1. Identify the affected generator and template
2. Fix the template or name resolver logic
3. Run smoke tests to see affected output
4. Update smoke test reference files if needed:
   ```bash
   DUMP_ACTUAL_DIR=$(pwd)/gluecodium/src/test/resources/smoke ./gradlew test
   ```
5. Run functional tests to verify fix

## Documentation Resources

- `docs/guide.md`: User guide for LimeIDL features
- `docs/lime_idl.md`: Complete LimeIDL syntax reference
- `docs/lime_attributes.md`: Attribute annotations reference
- `docs/internal/architecture.md`: Internal architecture overview
- `docs/internal/generators.md`: Generator implementation details
- `docs/internal/testing.md`: Testing approach
- `docs/js_binding_dev/`: JS/WebAssembly (embind) binding development — phased plan, spike
  results, and spike sources
- `examples/calculator/`: Simple example demonstrating features

## Validation

Gluecodium validates LIME models before generation:
- Type references validation
- Inheritance validation
- Function overloads validation
- Properties validation
- Structs validation
- External types validation
- Async operations validation
- Generic types validation

Validators are located in `gluecodium/src/main/java/com/here/gluecodium/validator/`.

## Caching

Output caching prevents overwriting unchanged files:
- Creates `.cache` directory in output folder
- Stores hash values for all generated files
- Removes obsolete files from previous runs
- Automatically deactivated on errors or invalid directories

Enable with `-cache` command line option.

## Naming Rules

Custom naming rules can be specified via `.properties` files. See `docs/naming_conventions.md` and functional tests in `functional-tests/namerules/`.

## External Types

External types allow using pre-existing types instead of generated code. Specified via `external` descriptor blocks in LimeIDL. See `docs/external_types.md`.

## Attributes

LimeIDL supports attributes for customizing generated code:
- `@Cpp`, `@Swift`, `@Java`, `@Kotlin`, `@Dart`: Language-specific settings
- `@Equatable`: Generate equality comparison
- `@Skip`: Skip generation for specific element/language
- `@EnableIf`: Conditional generation
- `@Deprecated`: Mark as deprecated

See `docs/lime_attributes.md` for complete reference.

## Contributing

- Sign off each commit (use `git commit -s` or add `Signed-off-by:` line)
- Run all tests before submitting PR
- Update documentation if adding new features
- Follow existing code style (Kotlin conventions)
- Use IntelliJ IDEA with provided syntax highlighter for LimeIDL

## License

Apache License 2.0. See `LICENSE` file for details.

Copyright (C) 2016-2025 HERE Europe B.V.

## Additional Notes

- **Language Boundary**: Objects passed between C++ and platform languages are wrapped/proxied automatically
- **Referential Equality**: Preserved across language boundaries (except for narrow interfaces in round-trip)
- **Error Handling**: C++ uses `Return<Value, Error>` type instead of exceptions; platforms use native exceptions
- **Nullability**: Marked with `?` suffix; mapped to `std::optional` in C++, optional types in Kotlin/Swift/Dart
- **Documentation Comments**: Use `//` for doc comments (preserved in generated code); `#` for local comments (discarded)