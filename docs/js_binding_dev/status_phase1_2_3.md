# JS/Embind Generator — Phase Status Report

## Phase 1 — LIME Model Layer Extensions ✅

**Commit**: `0f03d87e5` — "Add JS attribute type, name rules and generator options (Phase 1)"

### What was done

| Item | File | Status |
|------|------|--------|
| `JS("Js", NAME)` attribute type | `lime-runtime/.../LimeAttributeType.kt` | ✅ |
| `"Js" -> LimeAttributeType.JS` mapping | `lime-loader/.../AntlrLimeConverter.kt` | ✅ |
| `JS` added to `propagateParentAttributes()` | `lime-loader/.../AntlrLimeConverter.kt` | ✅ |
| JS naming rules (camelCase conventions) | `gluecodium/src/main/resources/namerules/js.properties` | ✅ new |
| `jsPackages`, `jsInternalPackages`, `jsModuleName`, `jsEmitTypeScriptStubs`, `jsNameRules` options | `gluecodium/.../GeneratorOptions.kt` | ✅ |
| CLI: `jspackage`, `jsintpackage`, `jsmodule`, `jsemittestubs`, `jsnamerules` | `gluecodium/.../OptionReader.kt` | ✅ |

### Verification
- `./gradlew :lime-loader:compileJava :lime-runtime:compileJava :gluecodium:compileKotlin` passes.

---

## Phases 2 & 3 — Generator Skeleton + Template System ✅

**Commit**: `ade34dc61` — "Add JsGenerator skeleton with embind templates (Phases 2-3)"

### What was done

**New package** `gluecodium/src/main/java/com/here/gluecodium/generator/js/`:

| File | Role |
|------|------|
| `JsGenerator.kt` | Main generator (`shortName = "js"`); dual model filtering (embind vs `.d.ts`), `@Cpp(Skip)` handling, primary-base selection, topological ordering of register functions in module init |
| `JsNameResolver.kt` | LIME → TypeScript type names for `.d.ts` stubs; basic type map incl. `bigint` for 64-bit ints; JSDoc comment resolution |
| `EmbindNameResolver.kt` | LIME → C++ names for embind binding code (wraps `CppNameResolver`, `forceFollowThrough`) |
| `JsNameRules.kt` | `@Js(Name=...)` support; flattened names for embind identifiers; output paths (`js/<pkg>/<Name>.d.ts`, `js/embind/<pkg>_<Name>.cpp`) |
| `JsCommentsProcessor.kt` | Markdown → JSDoc-compatible comments |
| `JsImport.kt` / `JsImportResolver.kt` | TS `import type` statement resolution |
| `EmbindIncludeResolver.kt` | C++ `#include` resolution for embind files |

**Registration**: `com.here.gluecodium.generator.js.JsGenerator` appended to the ServiceLoader
services file. `-g js` now works from the CLI.

**New templates** `gluecodium/src/main/resources/templates/js/`:
- Embind family: `EmbindFile`, `EmbindModuleInit` (single `EMSCRIPTEN_BINDINGS` block),
  `EmbindClass`/`EmbindInterface` (with single `base<>` slot per plan §5.3), `EmbindStruct`
  (`value_object`), `EmbindEnum`, `EmbindException`.
- Stub family: `JsStubHeader` (imports) + `JsStubClass`/`JsStubInterface`/`JsStubStruct`/
  `JsStubEnumeration`/`JsStubException`/`JsStubLambda`/`JsStubTypeAlias`.

### Verification
- Full compile passes.
- Unit test suite: only pre-existing failures remain (10 SmokeTest cases in
  `comments`/`name_rules` fixtures caused by a path-parsing environment issue with
  `/Volumes/Macintosh HD/...` spaces — reproduced on the base commit without these changes).

### Known limitations (by design at this stage)
- Templates emit skeleton registrations only: constructors/methods/properties/enumerators are not
  yet bound — that is Phase 4 (type mapping) and Phase 5 work.
- `std::optional<T>` / `Return<T,E>` casters not yet emitted (Phase 4 carry-forward from spike).
- No functional-test wiring yet (Phase 7/8).

## Phase 3 Documentation Follow-up - TypeScript JSDoc ✅

The initial Phase 3 implementation created `JsCommentsProcessor` and wired comment resolution
into `JsNameResolver`, but the `.d.ts` templates did not render the resolved comments and the
stub view model discarded child comment objects. Generated declarations therefore contained no
Lime documentation even though the resolver path existed.

The follow-up adds shared `JsStubDocumentation` and `JsStubFunctionDocumentation` partials and
preserves comments in `JsGenerator` view models. Generated declarations now include:

- top-level type, exception, lambda, and type-alias documentation;
- class/interface constructors, methods, and properties;
- named `@param`, `@returns`, and `@throws` tags;
- property extended descriptions, struct field comments, and enum enumerator comments; and
- JS-specific comment filtering and link resolution through the existing resolver.

### Verification

- `./gradlew :gluecodium:compileKotlin`
- Generated `Calculator.d.ts` from `examples/calculator/lime` using the JS generator.
- Confirmed the output contains calculator class and constructor descriptions, named parameter
  tags such as `@param first`, return and throws tags, and the resolved
  `Calculator.CalculatorError.RESULT_OUT_OF_BOUNDS` link.
