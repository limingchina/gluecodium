# Phase 1 — LIME Model Layer Extensions (Implementation)

> **Status**: ✅ Completed & committed (`python_bind` branch, commit `be4747f9a`)
> **Date**: 2026-07-12
> **Source plan**: `docs/python_pybind11_plan.md` (Phase 1, lines 64–118)
> **Build**: `lime-runtime`, `lime-loader`, `gluecodium` all compile with openjdk 17.

## Goal

Extend the LIME model and generator options so the future Python generator can be
driven by a `@Python(...)` attribute, Python-specific naming rules, and CLI/options
flags — without yet generating any code (that is Phase 2+).

## Changes

### 1.1 `PYTHON` attribute type — `lime-runtime/.../model/lime/LimeAttributeType.kt`

Added a new enum entry (value type `NAME`, matching `Cpp`/`Java`/`Kotlin`/`Swift`/`Dart`):

```kotlin
PYTHON("Python", LimeAttributeValueType.NAME),
```

This enables LimeIDL usage such as:

```lime
@Python(Name = "custom_name")
class MyClass { ... }

@Python(Skip)
class InternalOnly { ... }

@Python(Internal)
fun internalMethod() { ... }
```

### 1.2 Annotation converter — `lime-loader/.../loader/AntlrLimeConverter.kt`

- `convertAnnotationType()`: added `"Python" -> LimeAttributeType.PYTHON` so the
  `@Python` annotation is parsed (otherwise it throws `Unsupported attribute: 'Python'`).
- `propagateParentAttributes()`: extended the per-language propagation list from
  `listOf(JAVA, SWIFT, DART, KOTLIN)` to `listOf(JAVA, SWIFT, DART, KOTLIN, PYTHON)`,
  so `@Python(Internal)` / `@Python(Public)` set on a parent element are inherited by
  children.
- Added the import `import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON`
  (required for the unqualified `PYTHON` reference in the list above).

### 1.3 Python naming rules — `gluecodium/src/main/resources/namerules/python.properties` (new)

```properties
field=snake_case
parameter=snake_case
constant=UPPER_SNAKE_CASE
enumerator=UPPER_SNAKE_CASE
method=snake_case
property=snake_case
property.prefix.boolean=is
type=UpperCamelCase
error=UpperCamelCase
error.suffix=Error
join.infix=_
```

Mirrors the Dart rules but uses `snake_case` for fields/parameters/methods/properties
(Python PEP 8 convention) and an `Error` suffix for exceptions.

### 1.4 `GeneratorOptions` — `gluecodium/.../generator/common/GeneratorOptions.kt`

Added Python-related option fields:

```kotlin
var pythonPackages: List<String> = listOf(),
var pythonInternalPackages: List<String> = listOf(),
var pythonNameRules: Configuration =
    ConfigurationProperties.fromResource(Gluecodium::class.java, "/namerules/python.properties"),
var pythonModule: String = "generated",
```

### 1.5 CLI options — `gluecodium/.../cli/OptionReader.kt` (plan §2.4, pulled forward)

Added CLI options and wired them into `GeneratorOptions` (the options layer is needed
for end-to-end use, so it is implemented here rather than waiting for Phase 2):

| CLI option | Maps to `GeneratorOptions` |
|------------|----------------------------|
| `--pythonpackage` | `pythonPackages` (split on `.`) |
| `--python-internal-package` | `pythonInternalPackages` (split on `.`) |
| `--pythonmodule` | `pythonModule` |
| `--pythonnamerules` | `pythonNameRules` (via `readConfigFile`) |

## Verification

### Compile-time
- `./gradlew :lime-runtime:compileKotlin :lime-loader:compileKotlin :gluecodium:compileKotlin` → **success**.
- No generator is registered yet (plan §2.3), so the `ServiceLoader` is unaffected and
  the build remains green.

### Runtime (actual behavior, not just compilation)
Built the distribution (`./gradlew :gluecodium:installDist`) and exercised the new
code paths end-to-end:

1. **CLI options appear in `-help`** — confirmed all four are listed:
   ```
   -pythonintpackage,--python-internal-package <arg>
   -pythonmodule <arg>
   -pythonnamerules <arg>
   -pythonpackage <arg>
   ```

2. **`@Python` attribute parses** — ran `gluecodium -validate` on
   `docs/python_binding_dev/phase1/smoke_test_python.lime`, which uses
   `@Python(Name = "RenamedClass")`, `@Python(Skip)`, and `@Python(Internal)`.
   The run exited `0` with **no** `Unsupported attribute: 'Python'` error. (Only
   pre-existing doc-comment warnings appeared, unrelated to this change.) If any
   `@Python` variant were unsupported, `convertAnnotationType()` would have thrown.

3. **Naming-rules resource is packaged** — `namerules/python.properties` is present
   in the built `gluecodium` jar, so `GeneratorOptions.pythonNameRules` resolves at
   runtime via `ConfigurationProperties.fromResource(...)`.

### Test fixture
`docs/python_binding_dev/phase1/smoke_test_python.lime` is kept as a minimal fixture
covering the three `@Python` value forms (Name / Skip / Internal) for reuse in
later-phase verification (e.g. once `PythonGenerator` exists, confirm `SkippedClass`
and `MyClass.hiddenMethod` are filtered out).

## Notes / deviations from plan

- **CLI options pulled into Phase 1**: the plan lists them under Phase 2.4, but they are
  part of the options/CLI layer and are harmless to add now. They make the Python options
  usable as soon as the generator exists.
- **Generator registration deferred**: `PythonGenerator` is **not** registered in
  `META-INF/services/...Generator` (plan §2.3). Registering it now would break the build
  because the class does not exist yet. This happens in Phase 2.
- **Build toolchain**: the local `JAVA_HOME` had to point at openjdk 17
  (`/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home`); the previously set
  `openjdk@17` path was missing until reinstalled.

## Next step

Phase 2 — Generator skeleton: create `PythonGenerator` (+ name/include resolvers,
predicates, comments processor, overloads validator), the Mustache template directory,
and register the generator in `META-INF/services`.
